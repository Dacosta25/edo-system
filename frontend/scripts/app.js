console.log("DACOSTA JS UPDATED");

// ========================= API BASE URL =========================
const API_BASE_URL = "https://qqyckfigg8.execute-api.eu-west-2.amazonaws.com/Prod";

// ========================= DELETE FAILED ORDER =========================
async function deleteMessage(receiptHandle) {
  await fetch(`${API_BASE_URL}/failed-orders/${receiptHandle}`, { method: "DELETE" });
}

// ========================= FORM HANDLER =========================
function attachFormHandler() {
  const form = document.getElementById("order-form");
  if (form) {
    form.addEventListener("submit", submitOrder);
  }

  const refreshBtn = document.getElementById("refresh-orders-btn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", fetchOrders);
  }

  // Auto-refresh every 10 seconds
  setInterval(fetchOrders, 10000);

  // Initial load
  fetchOrders();
}

// ========================= SUBMIT ORDER =========================
async function submitOrder(event) {
  event.preventDefault();

  const productId = document.getElementById("product-select").value;
  const quantity = Number(document.getElementById("quantity-input").value);
  const customerId = document.getElementById("customer-id-input").value.trim();

  const orderPayload = {
    ItemID: productId,
    Quantity: quantity,
    CustomerID: customerId
  };

  const responsePanel = document.getElementById("response-panel");
  responsePanel.textContent = "Submitting order...";

  try {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(orderPayload)
    });

    const data = await response.json();
    renderResponse(data);

  } catch (error) {
    renderResponse({ error: "Unable to submit order", details: error.message });
  }
}

// ========================= RENDER API RESPONSE =========================
function renderResponse(data) {
  const panel = document.getElementById("response-panel");
  panel.textContent = JSON.stringify(data, null, 2);
}

// ========================= FETCH ORDERS =========================
async function fetchOrders() {
  const tbody = document.getElementById("orders-body");

  if (!tbody) {
    console.error("orders-body NOT FOUND in DOM");
    return;
  }

  tbody.innerHTML = `
    <tr><td colspan="4">Loading orders...</td></tr>
  `;

  try {
    const response = await fetch(`${API_BASE_URL}/orders`);
    const data = await response.json();

    console.log("AWS returned:", data);

    if (data.orders) return renderOrdersTable(data.orders);
    if (data.Items) return renderOrdersTable(data.Items);
    if (Array.isArray(data)) return renderOrdersTable(data);

    tbody.innerHTML = `
      <tr><td colspan="4">${JSON.stringify(data)}</td></tr>
    `;

  } catch (error) {
    tbody.innerHTML = `
      <tr><td colspan="4">Error loading orders: ${error.message}</td></tr>
    `;
  }
}

// ========================= TABLE RENDERER =========================
function renderOrdersTable(orders) {
  const tbody = document.getElementById("orders-body");

  if (!tbody) {
    console.error("orders-body NOT FOUND");
    return;
  }

  if (!Array.isArray(orders) || orders.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="4">No orders found.</td></tr>
    `;
    return;
  }

  let html = "";

  for (const order of orders) {
    html += `
      <tr>
        <td>${order.Quantity}</td>
        <td>${order.ItemID}</td>
        <td>${order.CustomerID}</td>
        <td>${order.OrderID}</td>
      </tr>
    `;
  }

  tbody.innerHTML = html;
}

// ========================= INIT =========================
document.addEventListener("DOMContentLoaded", attachFormHandler);