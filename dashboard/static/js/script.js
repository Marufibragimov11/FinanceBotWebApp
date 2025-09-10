// Use real data from Django instead of hardcoded demo data
const demoData = {
  balance: parseFloat(document.getElementById('balance-amount').textContent.replace('$', '').replace(',', '')) || 0,
  upcomingPayments: [
    { id: 1, title: 'Netflix', subtitle: 'Due Jan 15', amount: -15.99, icon: '🎬' },
    { id: 2, title: 'Spotify', subtitle: 'Due Jan 20', amount: -9.99, icon: '🎵' },
    { id: 3, title: 'Gym Membership', subtitle: 'Due Jan 25', amount: -49.99, icon: '💪' },
  ],
  transactions: [], // Will be populated by Django template
  categories: [], // Will be populated from window.analyticsData
};

function formatCurrency(value) {
  return value.toLocaleString(undefined, { style: 'currency', currency: 'USD' });
}

function renderBalance(balance) {
  const el = document.getElementById('balance-amount');
  const sumBal = document.getElementById('summary-balance');
  if (el) el.textContent = formatCurrency(balance);
  if (sumBal) sumBal.textContent = formatCurrency(balance);
}

function renderSummary(transactions) {
  const income = transactions.filter(t => t.amount > 0).reduce((a, b) => a + b.amount, 0);
  const expense = transactions.filter(t => t.amount < 0).reduce((a, b) => a + Math.abs(b.amount), 0);
  const incomeEl = document.getElementById('summary-income');
  const expenseEl = document.getElementById('summary-expense');
  if (incomeEl) incomeEl.textContent = formatCurrency(income);
  if (expenseEl) expenseEl.textContent = formatCurrency(expense);
}

function createListItem({ icon, title, subtitle, amount }) {
  const item = document.createElement('div');
  item.className = 'list-item';
  const iconEl = document.createElement('div');
  iconEl.className = 'item-icon';
  iconEl.textContent = icon;
  const textWrap = document.createElement('div');
  const titleEl = document.createElement('div');
  titleEl.className = 'item-title';
  titleEl.textContent = title;
  const subEl = document.createElement('div');
  subEl.className = 'item-subtitle';
  subEl.textContent = subtitle;
  textWrap.appendChild(titleEl);
  textWrap.appendChild(subEl);
  const amountEl = document.createElement('div');
  amountEl.className = 'item-amount ' + (amount < 0 ? 'negative' : 'positive');
  amountEl.textContent = (amount < 0 ? '-' : '+') + formatCurrency(Math.abs(amount));
  item.appendChild(iconEl);
  item.appendChild(textWrap);
  item.appendChild(amountEl);
  return item;
}

function renderList(containerId, items) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';
  items.forEach(item => container.appendChild(createListItem(item)));
}

function createUpcomingCard({ icon, title, subtitle, amount }) {
  const card = document.createElement('button');
  card.className = 'up-card';
  card.type = 'button';
  const iconEl = document.createElement('div');
  iconEl.className = 'up-card__icon';
  iconEl.textContent = icon;
  const mid = document.createElement('div');
  mid.style.display = 'grid';
  mid.style.justifyItems = 'center';
  mid.style.gap = '4px';
  const titleEl = document.createElement('div');
  titleEl.className = 'up-card__title';
  titleEl.textContent = title;
  const priceEl = document.createElement('div');
  priceEl.className = 'up-card__price';
  priceEl.textContent = (amount < 0 ? '-' : '+') + formatCurrency(Math.abs(amount));
  const dateEl = document.createElement('div');
  dateEl.className = 'up-card__date';
  dateEl.textContent = subtitle;
  mid.appendChild(titleEl);
  mid.appendChild(priceEl);
  card.appendChild(iconEl);
  card.appendChild(mid);
  card.appendChild(dateEl);
  return card;
}

function renderUpcomingRow(items) {
  const row = document.getElementById('upcoming-row');
  if (!row) return;
  row.innerHTML = '';
  items.forEach(i => row.appendChild(createUpcomingCard(i)));
}

function wireFilter(transactions) {
  const chips = document.querySelectorAll('.chip');
  const listContainerId = 'transactions-list';
  const update = (filter) => {
    chips.forEach(c => c.classList.toggle('chip--active', c.dataset.filter === filter));
    let filtered = transactions;
    if (filter === 'income') filtered = transactions.filter(t => t.amount > 0);
    if (filter === 'expense') filtered = transactions.filter(t => t.amount < 0);
    renderList(listContainerId, filtered);
  };
  chips.forEach(chip => chip.addEventListener('click', () => update(chip.dataset.filter)));
  update('all');
}

function drawDonut(canvasId, data, options = {}) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const total = data.reduce((a, b) => a + b.value, 0);
  const dpi = window.devicePixelRatio || 1;
  const size = canvas.width; // square
  canvas.width = size * dpi;
  canvas.height = size * dpi;
  ctx.scale(dpi, dpi);

  const center = size / 2;
  const radius = size / 2 - 20;
  const lineWidth = options.lineWidth || 28;
  let startAngle = -Math.PI / 2;

  // Background ring
  ctx.beginPath();
  ctx.lineWidth = lineWidth;
  ctx.strokeStyle = '#F3F4F6';
  ctx.arc(center, center, radius, 0, Math.PI * 2);
  ctx.stroke();

  // Segments
  data.forEach(segment => {
    const angle = (segment.value / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.lineCap = 'round';
    ctx.lineWidth = lineWidth;
    ctx.strokeStyle = segment.color;
    ctx.arc(center, center, radius, startAngle, startAngle + angle);
    ctx.stroke();
    startAngle += angle;
  });

  // Center label
  const centerWrap = document.getElementById('chart-center');
  if (centerWrap) {
    centerWrap.style.left = center - 1 + 'px';
    centerWrap.style.top = center - 1 + 'px';
    centerWrap.style.transform = 'translate(-50%, -50%)';
  }
  const centerValue = document.getElementById('chart-center-value');
  if (centerValue) centerValue.textContent = formatCurrency(total);

  // Legend
  const legend = document.getElementById('legend');
  if (legend) {
    legend.innerHTML = '';
    data.forEach(seg => {
      const row = document.createElement('div');
      row.className = 'legend-item';
      const dot = document.createElement('div');
      dot.className = 'legend-dot';
      dot.style.background = seg.color;
      const label = document.createElement('div');
      label.textContent = `${seg.name} • ${Math.round((seg.value / total) * 100)}%`;
      row.appendChild(dot);
      row.appendChild(label);
      legend.appendChild(row);
    });
  }
}

function main() {
  // Balance + Summary - use real data from Django
  const realBalance = parseFloat(document.getElementById('balance-amount').textContent.replace('$', '').replace(',', '')) || 0;
  renderBalance(realBalance);
  
  if (window.transactionsData) {
    renderSummary(window.transactionsData);
  } else {
    renderSummary(demoData.transactions);
  }

  // Upcoming + Transactions - use sample data for upcoming payments, real data for transactions
  renderUpcomingRow(demoData.upcomingPayments);
  
  if (window.transactionsData) {
    wireFilter(window.transactionsData);
  } else {
    wireFilter(demoData.transactions);
  }

  // Chart - use real analytics data from Django
  if (window.analyticsData) {
    const categories = Object.entries(window.analyticsData).map(([name, data]) => ({
      name: name,
      color: data.color,
      value: data.amount
    }));
    drawDonut('donutChart', categories, { lineWidth: 32 });
  } else {
    drawDonut('donutChart', demoData.categories, { lineWidth: 32 });
  }

  // Fab / Nav interactions
  const fab = document.getElementById('fab');
  if (fab) fab.addEventListener('click', () => alert('Add new transaction'));
}

document.addEventListener('DOMContentLoaded', main);


