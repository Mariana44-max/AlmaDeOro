/**
 * Utilidades para manejo del carrito
 * Sincroniza localStorage con backend para usuarios autenticados
 */

const CartUtils = {
  /**
   * Obtiene el user_id del token JWT actual
   */
  getCurrentUserId() {
    const token = localStorage.getItem('accessToken');
    if (!token) return null;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.user_id || payload.sub;
    } catch (e) {
      console.error('Error parsing token:', e);
      return null;
    }
  },

  /**
   * Obtiene la key del carrito para el usuario actual
   */
  getCartKey() {
    const userId = this.getCurrentUserId();
    return userId ? `cart_${userId}` : 'cart';
  },

  /**
   * Obtiene el carrito del localStorage
   */
  getCart() {
    try {
      const cartKey = this.getCartKey();
      const cartData = localStorage.getItem(cartKey);
      return cartData ? JSON.parse(cartData) : [];
    } catch (e) {
      console.error('Error getting cart:', e);
      return [];
    }
  },

  /**
   * Guarda el carrito en localStorage
   */
  setCart(cart) {
    try {
      const cartKey = this.getCartKey();
      localStorage.setItem(cartKey, JSON.stringify(cart));
    } catch (e) {
      console.error('Error setting cart:', e);
    }
  },

  /**
   * Limpia el carrito del usuario actual
   */
  clearCart() {
    const cartKey = this.getCartKey();
    localStorage.removeItem(cartKey);
  },

  /**
   * Limpia carritos de todos los usuarios (útil al logout)
   */
  clearAllCarts() {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith('cart_') || key === 'cart') {
        localStorage.removeItem(key);
      }
    });
  },

  /**
   * Migra carrito anónimo a carrito de usuario autenticado
   */
  migrateAnonymousCart() {
    const anonymousCart = localStorage.getItem('cart');
    if (anonymousCart) {
      const userId = this.getCurrentUserId();
      if (userId) {
        const userCartKey = `cart_${userId}`;
        const existingUserCart = localStorage.getItem(userCartKey);

        if (existingUserCart) {
          // Merge carritos
          const anonymous = JSON.parse(anonymousCart);
          const userCart = JSON.parse(existingUserCart);

          anonymous.forEach(anonItem => {
            const existingIndex = userCart.findIndex(item => item.id === anonItem.id);
            if (existingIndex >= 0) {
              // Suma cantidades si el producto ya existe
              userCart[existingIndex].quantity += anonItem.quantity;
            } else {
              userCart.push(anonItem);
            }
          });

          localStorage.setItem(userCartKey, JSON.stringify(userCart));
        } else {
          // Solo mueve el carrito anónimo
          localStorage.setItem(userCartKey, anonymousCart);
        }

        // Limpia carrito anónimo
        localStorage.removeItem('cart');
      }
    }
  },

  /**
   * Sincroniza el carrito de localStorage con el backend
   * @returns {Promise<boolean>} true si la sincronización fue exitosa
   */
  async syncCartToBackend() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.warn('No hay usuario autenticado, no se puede sincronizar');
      return false;
    }

    const cart = this.getCart();
    if (cart.length === 0) {
      return true; // No hay nada que sincronizar
    }

    try {
      // 1. Primero limpia el carrito del backend
      await fetch('http://127.0.0.1:8000/api/cart/clear/', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      // 2. Agrega cada item al carrito del backend
      for (const item of cart) {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/cart/items/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              product_id: item.id,
              quantity: item.quantity
            })
          });

          if (!response.ok) {
            const errorData = await response.json();
            console.error(`Error agregando item ${item.id}:`, errorData);
          }
        } catch (itemError) {
          console.error(`Error sincronizando item ${item.id}:`, itemError);
        }
      }

      console.log('✅ Carrito sincronizado con backend');
      return true;
    } catch (error) {
      console.error('❌ Error sincronizando carrito:', error);
      return false;
    }
  },

  /**
   * Carga el carrito desde el backend al localStorage
   * Útil después de login
   */
  async loadCartFromBackend() {
    const token = localStorage.getItem('accessToken');
    if (!token) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/api/cart/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const backendCart = await response.json();
        if (backendCart.items && backendCart.items.length > 0) {
          // Convierte formato backend a formato localStorage
          const localCart = backendCart.items.map(item => {
            // Obtener la primera imagen del producto
            const imageUrl = item.product.uploaded_images && item.product.uploaded_images.length > 0
              ? item.product.uploaded_images[0].image
              : 'img/default.jpg';

            return {
              id: item.product.id,
              name: item.product.name,
              price: parseFloat(item.product.price),
              image: imageUrl,
              quantity: item.quantity
            };
          });

          this.setCart(localCart);
          console.log('✅ Carrito cargado desde backend:', localCart.length, 'items');
        }
      }
    } catch (error) {
      console.error('Error cargando carrito desde backend:', error);
    }
  },

  /**
   * Calcula el total del carrito
   */
  getCartTotal() {
    const cart = this.getCart();
    return cart.reduce((total, item) => {
      const price = parseFloat(item.price) || 0;
      const quantity = parseInt(item.quantity) || 0;
      return total + (price * quantity);
    }, 0);
  },

  /**
   * Cuenta items en el carrito
   */
  getCartCount() {
    const cart = this.getCart();
    return cart.reduce((count, item) => count + (parseInt(item.quantity) || 0), 0);
  },

  /**
   * Agrega un producto al carrito
   */
  addToCart(product, quantity = 1) {
    const cart = this.getCart();
    const existingIndex = cart.findIndex(item => item.id === product.id);

    if (existingIndex >= 0) {
      cart[existingIndex].quantity += quantity;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image,
        quantity: quantity
      });
    }

    this.setCart(cart);
    return cart;
  },

  /**
   * Actualiza la cantidad de un producto
   */
  updateQuantity(productId, quantity) {
    const cart = this.getCart();
    const index = cart.findIndex(item => item.id === productId);

    if (index >= 0) {
      if (quantity <= 0) {
        cart.splice(index, 1);
      } else {
        cart[index].quantity = quantity;
      }
      this.setCart(cart);
    }

    return cart;
  },

  /**
   * Elimina un producto del carrito
   */
  removeFromCart(productId) {
    const cart = this.getCart();
    const filtered = cart.filter(item => item.id !== productId);
    this.setCart(filtered);
    return filtered;
  }
};

// Exportar para uso global
if (typeof window !== 'undefined') {
  window.CartUtils = CartUtils;
}
