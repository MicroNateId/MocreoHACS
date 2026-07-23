class MocreoCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this.innerHTML = `
        <style>
          ha-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 16px;
            color: #f8fafc;
            padding: 18px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
          }
          .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          }
          .title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
          }
          .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 12px;
          }
          .device-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(8px);
            border-radius: 12px;
            padding: 14px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
          }
          .device-card:hover {
            transform: translateY(-3px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 8px 20px rgba(56, 189, 248, 0.15);
          }
          .device-name {
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
          }
          .status-badge {
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.025em;
          }
          .online { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
          .offline { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }
          .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 6px;
            font-size: 0.85rem;
            color: #94a3b8;
          }
          .metric-val {
            font-weight: 700;
            color: #e2e8f0;
          }
          .temp-val { color: #38bdf8; font-size: 1.05rem; }
          .humidity-val { color: #818cf8; }
          .battery-val { color: #facc15; }
        </style>
        <ha-card>
          <div class="header">
            <div class="title">
              <ha-icon icon="mdi:shield-sun"></ha-icon>
              <span>MOCREO IoT Platform</span>
            </div>
          </div>
          <div class="device-grid" id="mocreo-grid"></div>
        </ha-card>
      `;
      this.content = this.querySelector('#mocreo-grid');
    }
    this.updateContent();
  }

  updateContent() {
    if (!this._hass || !this.content) return;
    
    const states = this._hass.states;
    const mocreoEntities = Object.keys(states).filter(id => id.includes('mocreo'));
    
    const devices = {};
    mocreoEntities.forEach(id => {
      const stateObj = states[id];
      const name = stateObj.attributes.friendly_name || id;
      const deviceName = name.replace(/( Temperature| Humidity| Battery| Online| Water Leak.*)/gi, '');
      
      if (!devices[deviceName]) {
        devices[deviceName] = {};
      }
      
      if (id.includes('temperature')) devices[deviceName].temp = stateObj.state;
      if (id.includes('humidity')) devices[deviceName].humidity = stateObj.state;
      if (id.includes('battery')) devices[deviceName].battery = stateObj.state;
      if (id.includes('online')) devices[deviceName].online = stateObj.state === 'on';
    });

    let html = '';
    Object.keys(devices).forEach(devName => {
      const dev = devices[devName];
      const isOnline = dev.online !== undefined ? dev.online : true;
      html += `
        <div class="device-card">
          <div class="device-name">
            <span>${devName}</span>
            <span class="status-badge ${isOnline ? 'online' : 'offline'}">${isOnline ? 'Online' : 'Offline'}</span>
          </div>
          ${dev.temp !== undefined ? `<div class="metric-row"><span>Temperature</span><span class="metric-val temp-val">${dev.temp}°</span></div>` : ''}
          ${dev.humidity !== undefined ? `<div class="metric-row"><span>Humidity</span><span class="metric-val humidity-val">${dev.humidity}%</span></div>` : ''}
          ${dev.battery !== undefined ? `<div class="metric-row"><span>Battery</span><span class="metric-val battery-val">${dev.battery}%</span></div>` : ''}
        </div>
      `;
    });

    if (html === '') {
      html = '<div style="color:#94a3b8; grid-column: 1/-1; text-align: center; padding: 20px;">No active MOCREO devices found.</div>';
    }

    this.content.innerHTML = html;
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('mocreo-card', MocreoCard);
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'mocreo-card',
  name: 'MOCREO IoT Family Card',
  description: 'A custom card to display all MOCREO environmental sensors, gateways, and live metrics.'
});
