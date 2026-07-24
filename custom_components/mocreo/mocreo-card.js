class MocreoCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  static getStubConfig() {
    return {};
  }

  static getConfigElement() {
    return document.createElement('div');
  }

  setConfig(config) {
    this._config = config;
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  render() {
    if (!this._hass) return;
    
    const root = this.shadowRoot;
    const states = this._hass.states || {};
    
    const devices = {};
    Object.keys(states).forEach(id => {
      const stateObj = states[id];
      const friendlyName = stateObj.attributes.friendly_name || id;
      
      const isMocreo = id.includes('mocreo') || 
                       friendlyName.toLowerCase().includes('mocreo') || 
                       friendlyName.toLowerCase().includes('guest_bed') || 
                       friendlyName.toLowerCase().includes('girls_bedroom') || 
                       friendlyName.toLowerCase().includes('master_bed');
                       
      if (!isMocreo) return;
      
      let devName = friendlyName
        .replace(/ (Temperature|Humidity|Battery|Online|Connectivity|Water Leak|Moisture|Base|Lora).*/gi, '')
        .trim();
        
      if (devName.toLowerCase().includes('master bedroom') || devName.toLowerCase().includes('master bed')) devName = 'Master Bedroom';
      else if (devName.toLowerCase().includes('girls bedroom')) devName = 'Girls Bedroom';
      else if (devName.toLowerCase().includes('guest bedroom') || devName.toLowerCase().includes('guest bed')) devName = 'Guest Bedroom';
      else if (devName.toLowerCase().includes('stairway')) devName = 'Stairway Sensor';

      if (!devices[devName]) {
        devices[devName] = {
          name: devName,
          temp: undefined,
          humidity: undefined,
          battery: undefined,
          online: undefined,
          last_updated: undefined
        };
      }
      
      if (id.includes('temperature') && !id.includes('battery') && !id.includes('online')) {
        devices[devName].temp = stateObj.state;
      }
      if (id.includes('humidity')) {
        devices[devName].humidity = stateObj.state;
      }
      if (id.includes('battery')) {
        devices[devName].battery = stateObj.state;
      }
      if (id.includes('online') || stateObj.attributes.device_class === 'connectivity') {
        devices[devName].online = stateObj.state === 'on' || stateObj.state === 'true';
      }
      if (stateObj.last_updated) {
        devices[devName].last_updated = stateObj.last_updated;
      }
    });

    let totalDevices = Object.keys(devices).length;
    let onlineCount = 0;

    let devicesHtml = '';
    Object.keys(devices).sort().forEach(devName => {
      const dev = devices[devName];
      const isOnline = dev.online !== undefined ? dev.online : (dev.temp !== 'unavailable' && dev.temp !== undefined);
      if (isOnline) onlineCount++;

      const tempDisplay = (dev.temp && dev.temp !== 'unavailable') ? `${dev.temp}°F` : 'N/A';
      const humidityDisplay = (dev.humidity && dev.humidity !== 'unavailable') ? `${dev.humidity}%` : 'N/A';
      const batteryDisplay = (dev.battery && dev.battery !== 'unavailable') ? `${dev.battery}%` : 'N/A';

      devicesHtml += `
        <div class="device-card">
          <div class="device-name">
            <span>${devName}</span>
            <span class="status-badge ${isOnline ? 'online' : 'offline'}">${isOnline ? 'Online' : 'Offline'}</span>
          </div>
          <div class="metrics-grid">
            <div class="metric-box">
              <span class="metric-label">Temp</span>
              <span class="metric-val temp-val">${tempDisplay}</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Humidity</span>
              <span class="metric-val humidity-val">${humidityDisplay}</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Battery</span>
              <span class="metric-val battery-val">${batteryDisplay}</span>
            </div>
          </div>
        </div>
      `;
    });

    if (devicesHtml === '') {
      devicesHtml = '<div style="color:#94a3b8; grid-column: 1/-1; text-align: center; padding: 20px;">Searching for MOCREO devices...</div>';
    }

    root.innerHTML = `
      <style>
        :host {
          display: block;
        }
        ha-card {
          background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
          border-radius: 16px;
          color: #f8fafc;
          padding: 18px;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(255, 255, 255, 0.1);
          font-family: 'Inter', system-ui, -apple-system, sans-serif;
          display: block;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .title-group {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .title {
          font-size: 1.2rem;
          font-weight: 700;
          color: #38bdf8;
        }
        .summary-badge {
          font-size: 0.8rem;
          padding: 4px 10px;
          border-radius: 12px;
          background: rgba(56, 189, 248, 0.15);
          color: #38bdf8;
          border: 1px solid rgba(56, 189, 248, 0.3);
          font-weight: 600;
        }
        .device-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
          gap: 12px;
        }
        .device-card {
          background: rgba(30, 41, 59, 0.7);
          border-radius: 12px;
          padding: 14px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          transition: all 0.2s ease;
        }
        .device-card:hover {
          border-color: rgba(56, 189, 248, 0.4);
          transform: translateY(-2px);
        }
        .device-name {
          font-weight: 600;
          font-size: 0.95rem;
          margin-bottom: 12px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          color: #f1f5f9;
        }
        .status-badge {
          font-size: 0.75rem;
          padding: 2px 8px;
          border-radius: 10px;
          font-weight: 600;
        }
        .online { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
        .offline { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }
        .metrics-grid {
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          gap: 6px;
          text-align: center;
        }
        .metric-box {
          background: rgba(15, 23, 42, 0.6);
          padding: 6px 4px;
          border-radius: 8px;
          border: 1px solid rgba(255, 255, 255, 0.04);
        }
        .metric-label {
          display: block;
          font-size: 0.7rem;
          color: #94a3b8;
          text-transform: uppercase;
          margin-bottom: 2px;
        }
        .metric-val {
          font-weight: 700;
          font-size: 0.9rem;
        }
        .temp-val { color: #38bdf8; }
        .humidity-val { color: #818cf8; }
        .battery-val { color: #facc15; }
      </style>
      <ha-card>
        <div class="header">
          <div class="title-group">
            <span class="title">MOCREO Environmental Sensors</span>
          </div>
          <span class="summary-badge">${onlineCount} / ${totalDevices} Online</span>
        </div>
        <div class="device-grid">
          ${devicesHtml}
        </div>
      </ha-card>
    `;
  }

  getCardSize() {
    return 3;
  }
}

if (!customElements.get('mocreo-card')) {
  customElements.define('mocreo-card', MocreoCard);
}

window.customCards = window.customCards || [];
if (!window.customCards.some(c => c.type === 'mocreo-card')) {
  window.customCards.push({
    type: 'mocreo-card',
    name: 'MOCREO IoT Family Card',
    description: 'A custom card to display all MOCREO environmental sensors, gateways, and live metrics.'
  });
}
