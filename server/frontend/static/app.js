// Best Cars Dealership - Client Application
let currentDealers = [];
let allCars = [];

// Determine current route on load
window.addEventListener('DOMContentLoaded', () => {
  checkAuthStatus();
  handleRoute();
});

window.addEventListener('popstate', () => {
  handleRoute();
});

function navigateTo(e, path) {
  if (e) e.preventDefault();
  window.history.pushState({}, '', path);
  handleRoute();
}

function handleRoute() {
  const path = window.location.pathname;
  const searchParams = new URLSearchParams(window.location.search);
  const stateParam = searchParams.get('state');

  if (path.startsWith('/dealer/')) {
    const parts = path.split('/');
    const dealerId = parts[2];
    renderDealerDetailsView(dealerId);
  } else if (path.startsWith('/postreview/')) {
    const parts = path.split('/');
    const dealerId = parts[2];
    renderPostReviewView(dealerId);
  } else {
    renderHomeView(stateParam || 'all');
  }
}

// Authentication Helpers
function getLoggedInUser() {
  return sessionStorage.getItem('username');
}

function checkAuthStatus() {
  const username = getLoggedInUser();
  const loggedOutBlock = document.getElementById('nav-auth-loggedout');
  const loggedInBlock = document.getElementById('nav-auth-loggedin');
  const usernameSpan = document.getElementById('current-username');

  if (username) {
    loggedOutBlock.style.display = 'none';
    loggedInBlock.style.display = 'flex';
    usernameSpan.textContent = username;
  } else {
    loggedOutBlock.style.display = 'flex';
    loggedInBlock.style.display = 'none';
  }
}

// Modal Handlers
function openLoginModal() {
  document.getElementById('login-modal').style.display = 'flex';
  document.getElementById('login-error').style.display = 'none';
}

function closeLoginModal() {
  document.getElementById('login-modal').style.display = 'none';
}

function openRegisterModal() {
  document.getElementById('register-modal').style.display = 'flex';
  document.getElementById('register-error').style.display = 'none';
  document.getElementById('register-success').style.display = 'none';
}

function closeRegisterModal() {
  document.getElementById('register-modal').style.display = 'none';
}

// Login API
async function handleLoginSubmit(e) {
  e.preventDefault();
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  const errBox = document.getElementById('login-error');

  try {
    const res = await fetch('/djangoapp/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userName: username, password: password })
    });
    const data = await res.json();
    if (data.status === 'Authenticated') {
      sessionStorage.setItem('username', data.userName);
      closeLoginModal();
      checkAuthStatus();
      handleRoute();
    } else {
      errBox.textContent = data.error || 'Invalid credentials.';
      errBox.style.display = 'block';
    }
  } catch (err) {
    errBox.textContent = 'Server connection error.';
    errBox.style.display = 'block';
  }
}

// Register API
async function handleRegisterSubmit(e) {
  e.preventDefault();
  const username = document.getElementById('reg-username').value.trim();
  const firstName = document.getElementById('reg-firstname').value.trim();
  const lastName = document.getElementById('reg-lastname').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;
  const errBox = document.getElementById('register-error');
  const successBox = document.getElementById('register-success');

  try {
    const res = await fetch('/djangoapp/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userName: username,
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
      })
    });
    const data = await res.json();
    if (data.status === 'Authenticated') {
      sessionStorage.setItem('username', data.userName);
      successBox.textContent = 'Registration successful! Welcome!';
      successBox.style.display = 'block';
      setTimeout(() => {
        closeRegisterModal();
        checkAuthStatus();
        handleRoute();
      }, 1000);
    } else {
      errBox.textContent = data.error || 'Registration failed.';
      errBox.style.display = 'block';
    }
  } catch (err) {
    errBox.textContent = 'Server connection error.';
    errBox.style.display = 'block';
  }
}

// Logout API
async function performLogout() {
  try {
    await fetch('/djangoapp/logout');
  } catch (err) {}
  sessionStorage.removeItem('username');
  checkAuthStatus();
  handleRoute();
}

// HOME VIEW: Dealerships Directory
async function renderHomeView(selectedState = 'all') {
  const root = document.getElementById('app-root');
  root.innerHTML = `
    <section class="hero-banner">
      <h1>Dealership Branches Across the United States</h1>
      <p>Discover reputable authorized car dealership partners, inspect vehicle models, view genuine verified buyer ratings, and filter branches nationwide.</p>
    </section>

    <section class="filter-container">
      <div class="filter-left">
        <label for="state-filter">Filter by State:</label>
        <select id="state-filter" class="state-select" onchange="onStateFilterChange(this.value)">
          <option value="all" ${selectedState === 'all' ? 'selected' : ''}>All States</option>
          <option value="Kansas" ${selectedState.toLowerCase() === 'kansas' || selectedState.toUpperCase() === 'KS' ? 'selected' : ''}>Kansas (KS)</option>
          <option value="California" ${selectedState.toLowerCase() === 'california' || selectedState.toUpperCase() === 'CA' ? 'selected' : ''}>California (CA)</option>
          <option value="Texas" ${selectedState.toLowerCase() === 'texas' || selectedState.toUpperCase() === 'TX' ? 'selected' : ''}>Texas (TX)</option>
          <option value="New York" ${selectedState.toLowerCase() === 'new york' || selectedState.toUpperCase() === 'NY' ? 'selected' : ''}>New York (NY)</option>
          <option value="Florida" ${selectedState.toLowerCase() === 'florida' || selectedState.toUpperCase() === 'FL' ? 'selected' : ''}>Florida (FL)</option>
          <option value="Illinois" ${selectedState.toLowerCase() === 'illinois' || selectedState.toUpperCase() === 'IL' ? 'selected' : ''}>Illinois (IL)</option>
        </select>
      </div>
      <div class="dealer-count-badge" id="dealers-count-badge">Loading dealerships...</div>
    </section>

    <div class="dealers-table-wrapper">
      <table class="dealers-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>State</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="dealers-tbody">
          <tr><td colspan="7" style="text-align: center; padding: 2rem;">Loading dealership records...</td></tr>
        </tbody>
      </table>
    </div>
  `;

  // Fetch dealerships from Django backend
  const url = selectedState && selectedState !== 'all' 
    ? `/djangoapp/get_dealers/${selectedState}`
    : `/djangoapp/get_dealers`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    currentDealers = Array.isArray(data) ? data : (data.dealers || []);
    renderDealersTable(currentDealers);
  } catch (err) {
    document.getElementById('dealers-tbody').innerHTML = `
      <tr><td colspan="7" style="text-align: center; color: #dc2626; padding: 2rem;">Error loading dealerships from server.</td></tr>
    `;
  }
}

function onStateFilterChange(state) {
  if (state === 'all') {
    window.history.pushState({}, '', '/');
  } else {
    window.history.pushState({}, '', `/?state=${encodeURIComponent(state)}`);
  }
  renderHomeView(state);
}

function renderDealersTable(dealers) {
  const tbody = document.getElementById('dealers-tbody');
  const countBadge = document.getElementById('dealers-count-badge');
  const user = getLoggedInUser();

  if (countBadge) {
    countBadge.textContent = `Showing ${dealers.length} dealership${dealers.length === 1 ? '' : 's'}`;
  }

  if (dealers.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: #64748b;">No dealerships found for this state selection.</td></tr>`;
    return;
  }

  tbody.innerHTML = dealers.map(d => `
    <tr>
      <td style="font-weight: 700; color: #0284c7;">#${d.id}</td>
      <td style="font-weight: 700; color: #0f172a;">${d.full_name || d.short_name}</td>
      <td>${d.city}</td>
      <td>${d.address}</td>
      <td>${d.zip}</td>
      <td><span class="state-badge">${d.state} (${d.st || d.state})</span></td>
      <td>
        <div class="action-btn-group">
          <a href="/dealer/${d.id}" class="btn-view-dealer" onclick="navigateTo(event, '/dealer/${d.id}')">View Reviews</a>
          ${user ? `<a href="/postreview/${d.id}" class="btn-review-dealer" onclick="navigateTo(event, '/postreview/${d.id}')">Review Dealer</a>` : ''}
        </div>
      </td>
    </tr>
  `).join('');
}

// DEALER DETAILS & REVIEWS VIEW
async function renderDealerDetailsView(dealerId) {
  const root = document.getElementById('app-root');
  const user = getLoggedInUser();

  root.innerHTML = `
    <div style="margin-bottom: 1.5rem;">
      <a href="/" onclick="navigateTo(event, '/')" style="color: #0284c7; text-decoration: none; font-weight: 600;">← Back to Dealerships</a>
    </div>
    <div id="dealer-header-placeholder">Loading dealer info...</div>
    <div class="reviews-section-title">
      <h3 style="font-size: 1.5rem; color: #0f172a;">Customer Reviews & Sentiment</h3>
      ${user ? `<a href="/postreview/${dealerId}" class="btn-review-dealer" onclick="navigateTo(event, '/postreview/${dealerId}')">Write a Review</a>` : ''}
    </div>
    <div id="reviews-container" class="reviews-grid">
      <p style="color: #64748b;">Loading reviews...</p>
    </div>
  `;

  try {
    // 1. Fetch dealer details
    const dealerRes = await fetch(`/djangoapp/dealer/${dealerId}`);
    const dealerData = await dealerRes.json();
    const dealer = Array.isArray(dealerData) ? dealerData[0] : ((dealerData.dealer && dealerData.dealer[0]) || dealerData);

    if (dealer) {
      document.getElementById('dealer-header-placeholder').innerHTML = `
        <div class="dealer-detail-card">
          <div class="dealer-info">
            <h2>${dealer.full_name || dealer.short_name}</h2>
            <div class="dealer-meta">
              <span>📍 ${dealer.address}, ${dealer.city}, ${dealer.state} ${dealer.zip}</span>
              <span>📞 (800) 555-CARS</span>
            </div>
          </div>
          <div>
            <span class="state-badge" style="font-size: 1rem; padding: 0.5rem 1rem;">Branch ID: #${dealer.id}</span>
          </div>
        </div>
      `;
    }

    // 2. Fetch reviews
    const revRes = await fetch(`/djangoapp/get_reviews/${dealerId}`);
    const revData = await revRes.json();
    const reviews = Array.isArray(revData) ? revData : (revData.reviews || []);

    const reviewsContainer = document.getElementById('reviews-container');
    if (reviews.length === 0) {
      reviewsContainer.innerHTML = `
        <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0; grid-column: 1 / -1; text-align: center; color: #64748b;">
          No reviews yet for this dealership. Be the first to submit a review!
        </div>
      `;
    } else {
      reviewsContainer.innerHTML = reviews.map(r => {
        const sentiment = (r.sentiment || 'neutral').toLowerCase();
        const badgeClass = sentiment === 'positive' 
          ? 'sentiment-positive' 
          : sentiment === 'negative' 
            ? 'sentiment-negative' 
            : 'sentiment-neutral';
        const sentimentIcon = sentiment === 'positive' ? '👍' : sentiment === 'negative' ? '👎' : '😐';

        return `
          <div class="review-card">
            <div>
              <div class="review-top">
                <span class="reviewer-name">${r.name || 'Verified Customer'}</span>
                <span class="sentiment-badge ${badgeClass}">${sentimentIcon} ${sentiment}</span>
              </div>
              <p class="review-body">"${r.review}"</p>
            </div>
            <div>
              ${r.car_make ? `
                <div class="review-car-tag">
                  🚗 ${r.car_year || ''} ${r.car_make} ${r.car_model || ''}
                  ${r.purchase_date ? ` • Purchased: ${r.purchase_date}` : ''}
                </div>
              ` : ''}
            </div>
          </div>
        `;
      }).join('');
    }
  } catch (err) {
    document.getElementById('reviews-container').innerHTML = `<p style="color: red;">Error fetching reviews.</p>`;
  }
}

// POST REVIEW VIEW
async function renderPostReviewView(dealerId) {
  const root = document.getElementById('app-root');
  const user = getLoggedInUser();

  if (!user) {
    root.innerHTML = `
      <div style="text-align: center; padding: 3rem; background: white; border-radius: 12px; border: 1px solid #e2e8f0;">
        <h3 style="margin-bottom: 1rem;">Authentication Required</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">You must be logged in to post a review for this dealership.</p>
        <button class="nav-btn btn-login" onclick="openLoginModal()">Login Now</button>
      </div>
    `;
    return;
  }

  root.innerHTML = `
    <div style="margin-bottom: 1.5rem;">
      <a href="/dealer/${dealerId}" onclick="navigateTo(event, '/dealer/${dealerId}')" style="color: #0284c7; text-decoration: none; font-weight: 600;">← Back to Dealer Reviews</a>
    </div>

    <div class="post-review-container">
      <h2 style="margin-bottom: 0.5rem; color: #0f172a;">Post a Review for Dealer #${dealerId}</h2>
      <p style="color: #64748b; margin-bottom: 1.8rem; font-size: 0.95rem;">Share your vehicle purchase or service experience. Our system will analyze the sentiment of your feedback.</p>

      <form id="post-review-form" onsubmit="handleReviewSubmit(event, ${dealerId})">
        <div id="review-status-box" style="display: none;"></div>

        <div class="form-group">
          <label for="review-content">Your Review</label>
          <textarea id="review-content" rows="4" required placeholder="Write your honest review here... (e.g. Fantastic services and very courteous staff)"></textarea>
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="review-purchase" onchange="togglePurchaseFields(this.checked)">
          <label for="review-purchase">I purchased a car from this dealership</label>
        </div>

        <div id="purchase-details" style="display: none;">
          <div class="form-row">
            <div class="form-group">
              <label for="car-make-select">Car Make</label>
              <select id="car-make-select" onchange="onCarMakeSelected(this.value)">
                <option value="">Select Car Make</option>
              </select>
            </div>
            <div class="form-group">
              <label for="car-model-select">Car Model</label>
              <select id="car-model-select">
                <option value="">Select Car Model</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="car-year-input">Car Year</label>
              <input type="number" id="car-year-input" min="2015" max="2027" value="2024">
            </div>
            <div class="form-group">
              <label for="purchase-date-input">Purchase Date</label>
              <input type="date" id="purchase-date-input">
            </div>
          </div>
        </div>

        <button type="submit" class="submit-action-btn" style="background-color: #10b981;">Submit Review</button>
      </form>
    </div>
  `;

  // Fetch cars list to populate dropdown
  try {
    const res = await fetch('/djangoapp/get_cars');
    const data = await res.json();
    allCars = data.CarModels || [];

    const makeSelect = document.getElementById('car-make-select');
    const makes = [...new Set(allCars.map(c => c.CarMake))];
    makeSelect.innerHTML = `<option value="">Select Car Make</option>` + makes.map(m => `<option value="${m}">${m}</option>`).join('');
  } catch (err) {}
}

function togglePurchaseFields(checked) {
  document.getElementById('purchase-details').style.display = checked ? 'block' : 'none';
}

function onCarMakeSelected(selectedMake) {
  const modelSelect = document.getElementById('car-model-select');
  if (!selectedMake) {
    modelSelect.innerHTML = `<option value="">Select Car Model</option>`;
    return;
  }
  const filteredModels = allCars.filter(c => c.CarMake === selectedMake);
  modelSelect.innerHTML = filteredModels.map(c => `<option value="${c.CarModel}">${c.CarModel} (${c.Type})</option>`).join('');
}

async function handleReviewSubmit(e, dealerId) {
  e.preventDefault();
  const user = getLoggedInUser() || 'Anonymous';
  const reviewText = document.getElementById('review-content').value.trim();
  const purchased = document.getElementById('review-purchase').checked;
  const carMake = purchased ? document.getElementById('car-make-select').value : '';
  const carModel = purchased ? document.getElementById('car-model-select').value : '';
  const carYear = purchased ? parseInt(document.getElementById('car-year-input').value, 10) : 2024;
  const purchaseDate = purchased ? document.getElementById('purchase-date-input').value : '';

  const statusBox = document.getElementById('review-status-box');

  const payload = {
    dealership: dealerId,
    name: user,
    review: reviewText,
    purchase: purchased,
    purchase_date: purchaseDate,
    car_make: carMake,
    car_model: carModel,
    car_year: carYear
  };

  try {
    const res = await fetch('/djangoapp/add_review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.status === 200) {
      statusBox.className = 'success-badge';
      statusBox.textContent = 'Review submitted successfully! Redirecting...';
      statusBox.style.display = 'block';
      setTimeout(() => {
        navigateTo(null, `/dealer/${dealerId}`);
      }, 1200);
    } else {
      statusBox.className = 'error-badge';
      statusBox.textContent = data.error || 'Failed to submit review.';
      statusBox.style.display = 'block';
    }
  } catch (err) {
    statusBox.className = 'error-badge';
    statusBox.textContent = 'Network error while submitting review.';
    statusBox.style.display = 'block';
  }
}
