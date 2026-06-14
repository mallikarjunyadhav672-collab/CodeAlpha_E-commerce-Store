let products = [];
let cart = [];
let wishlist = new Set();
let activeFilter = 'all';
let searchTerm = '';

async function loadProducts() {
  try {
    const res = await fetch('/api/products/');
    const data = await res.json();
    products = data.products || [];
    renderProducts();
  } catch (e) { console.warn('Could not load products', e); }
}

function renderProducts() {
  const grid = document.getElementById('productsGrid');
  if (!grid) return; // nothing to render on pages without products grid
  let filtered = products.filter(p => {
    const matchCat = activeFilter === 'all' || p.category === activeFilter;
    const matchSearch = p.name.toLowerCase().includes(searchTerm) || p.brand.toLowerCase().includes(searchTerm);
    return matchCat && matchSearch;
  });
  const placeholder = '/static/img/placeholder.svg';
  grid.innerHTML = filtered.map(p => `
    <div class="product-card">
      <div class="product-img">
        <img src="${p.img || placeholder}" alt="${p.name}" onerror="this.src='${placeholder}'">
        ${p.badge ? `<span class="badge ${p.badge}">${p.badge.toUpperCase()}</span>` : ''}
        <button class="wishlist-btn ${wishlist.has(p.id)?'active':''}" onclick="toggleWishlist(${p.id})">
          ${wishlist.has(p.id)?'❤️':'🤍'}
        </button>
      </div>
      <div class="product-info">
        <div class="product-brand">${p.brand}</div>
        <div class="product-name">${p.name}</div>
        <div style="font-size:.78rem;color:var(--muted);margin-top:4px;">
          <span class="stars">${'★'.repeat(Math.floor(p.rating))}</span> ${p.rating} (${p.reviews})
        </div>
        <div class="product-meta">
          <div class="product-price">
            ₹${Number(p.price).toLocaleString('en-IN')}
            ${p.oldPrice ? `<span class="old">₹${Number(p.oldPrice).toLocaleString('en-IN')}</span>` : ''}
          </div>
        </div>
        <button class="add-to-cart" onclick="addToCart(${p.id})">Add to Cart</button>
      </div>
    </div>
  `).join('');
}

function setFilter(btn, cat) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  activeFilter = cat;
  renderProducts();
}

function filterByCategory(cat) {
  activeFilter = cat;
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active', b.textContent.toLowerCase().includes(cat) || (cat==='all' && b.textContent==='All'));
  });
  renderProducts();
  document.getElementById('products').scrollIntoView({behavior:'smooth'});
}

function filterProducts() {
  searchTerm = document.getElementById('searchInput').value.toLowerCase();
  renderProducts();
}

// --- Server sync helpers ---
async function fetchServerCart() {
  try {
    const res = await fetch('/api/cart/');
    const data = await res.json();
    const serverCart = data.cart || {};
    cart = [];
    for (const [pid, qty] of Object.entries(serverCart)) {
      const p = products.find(x => x.id === Number(pid));
      if (p && qty > 0) cart.push({ ...p, qty: Number(qty) });
    }
    updateCartUI();
  } catch (e) { console.warn('Could not fetch server cart', e); }
}

async function fetchServerWishlist() {
  try {
    const res = await fetch('/api/wishlist/');
    const data = await res.json();
    const wl = new Set((data.wishlist || []).map(x => Number(x)));
    wishlist = wl;
    renderProducts();
  } catch (e) { console.warn('Could not fetch wishlist', e); }
}

async function syncAddToCart(id, qty = 1) {
  try {
    await fetch('/api/cart/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: id, qty: qty })
    });
  } catch (e) { console.warn('Cart sync failed', e); }
}

async function syncToggleWishlist(id) {
  try {
    await fetch('/api/wishlist/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: id })
    });
  } catch (e) { console.warn('Wishlist sync failed', e); }
}

// UI actions that sync with server
async function addToCart(id) {
  const p = products.find(x => x.id === id);
  const ex = cart.find(x => x.id === id);
  if (ex) ex.qty++;
  else cart.push({ ...p, qty: 1 });
  updateCartUI();
  showToast(`${p.name} added to cart! 🛍`);
  syncAddToCart(id, 1);
}

function toggleWishlist(id) {
  if (wishlist.has(id)) wishlist.delete(id);
  else { wishlist.add(id); showToast('Added to Wishlist ❤️'); }
  renderProducts();
  syncToggleWishlist(id);
}

function changeQty(id, delta) {
  const i = cart.find(x => x.id===id);
  if (!i) return;
  i.qty += delta;
  if (i.qty <= 0) {
    syncAddToCart(id, - (i.qty * 0 + 1) );
    cart = cart.filter(x => x.id!==id);
  } else {
    syncAddToCart(id, delta);
  }
  updateCartUI();
}

function removeItem(id) {
  const item = cart.find(x => x.id===id);
  if (item) {
    syncAddToCart(id, -item.qty);
  }
  cart = cart.filter(x => x.id!==id);
  updateCartUI();
}

async function checkout() {
  try {
    for (const i of cart) {
      await fetch('/api/cart/', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: i.id, qty: -i.qty })
      });
    }
  } catch (e) { console.warn('Checkout sync partial failure', e); }
  showToast('Order placed! 🎉 Thank you for shopping with LUXE!');
  cart = [];
  updateCartUI();
  toggleCart();
}

function updateCartUI() {
  const count = cart.reduce((s,i) => s+i.qty, 0);
  document.getElementById('cartCount').textContent = count;
  const itemsEl = document.getElementById('cartItems');
  if (!cart.length) {
    itemsEl.innerHTML = `<div class="empty-cart"><div class="icon">🛒</div><p>Your cart is empty</p><p style="margin-top:8px;font-size:.83rem">Add some amazing products!</p></div>`;
    document.getElementById('cartFooter').style.display = 'none';
    return;
  }
  document.getElementById('cartFooter').style.display = 'block';
  const placeholder = '/static/img/placeholder.svg';
  itemsEl.innerHTML = cart.map(i => `
    <div class="cart-item">
      <img src="${i.img || placeholder}" alt="${i.name}" onerror="this.src='${placeholder}'">
      <div class="cart-item-info">
        <div class="cart-item-brand">${i.brand}</div>
        <div class="cart-item-name">${i.name}</div>
        <div class="cart-item-bottom">
          <span class="cart-item-price">₹${(i.price*i.qty).toLocaleString('en-IN')}</span>
          <div class="qty-ctrl">
            <button class="qty-btn" onclick="changeQty(${i.id},-1)">-</button>
            <span class="qty-val">${i.qty}</span>
            <button class="qty-btn" onclick="changeQty(${i.id},1)">+</button>
          </div>
        </div>
        <button class="remove-item" onclick="removeItem(${i.id})">Remove</button>
      </div>
    </div>
  `).join('');
  const sub = cart.reduce((s,i) => s+i.price*i.qty, 0);
  document.getElementById('cartSubtotal').textContent = '₹'+sub.toLocaleString('en-IN');
  document.getElementById('cartTotal').textContent = '₹'+sub.toLocaleString('en-IN');
}

function toggleCart() {
  document.getElementById('cartDrawer').classList.toggle('open');
  document.getElementById('cartOverlay').classList.toggle('open');
  updateCartUI();
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// Initialize
function setActiveNav() {
  try {
    const path = location.pathname.replace(/\/+$|^\/+/g, '/') || '/';
    document.querySelectorAll('.nav-links a').forEach(a => {
      const href = new URL(a.href, location.origin).pathname;
      a.classList.toggle('active', href === location.pathname || (href !== '/' && location.pathname.startsWith(href)));
    });
  } catch (e) { /* ignore */ }
}
    
// Newsletter submit handler (used by About/footer forms)
async function submitNewsletter(e){
  if(e && e.preventDefault) e.preventDefault();
  let email;
  try{
    if(e && e.target){
      const el = e.target.querySelector('[name=email]') || document.getElementById('newsletterEmail');
      email = el && el.value;
    }
  }catch(err){}
  if(!email) return showToast('Enter a valid email');
  try{
    const res = await fetch('/api/newsletter/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email})});
    if(res.ok) showToast('Subscribed — thank you!');
    else{
      const data = await res.json().catch(()=>({error:'Subscription failed'}));
      showToast(data.error || 'Subscription failed');
    }
  }catch(err){ showToast('Subscription failed'); }
  return false;
}

loadProducts().then(() => { fetchServerCart(); fetchServerWishlist(); setActiveNav(); });
