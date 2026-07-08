const API_URL = "https://qqyckfigg8.execute-api.eu-west-2.amazonaws.com/Prod";

async function loadFailedOrders() {
  const container = document.getElementById("failed-orders-container");

  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    if (data.length === 0) {
      container.innerHTML = "<p>No failed orders 🎉</p>";
      return;
    }

    container.innerHTML = data.map(msg => `
      <div class="failed-order">
        <h3>Message ID: ${msg.messageId}</h3>
        <pre>${JSON.stringify(msg.order, null, 2)}</pre>

        <button onclick="deleteMessage('${msg.receiptHandle}')">
          Delete
        </button>
      </div>
    `).join("");

  } catch (err) {
    container.innerHTML = `<p>Error loading failed orders: ${err}</p>`;
  }
}

async function deleteMessage(receiptHandle) {
  await fetch(`${API_URL}/${receiptHandle}`, {
    method: "DELETE"
  });

  loadFailedOrders();
}

loadFailedOrders();
