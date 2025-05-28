import './Graph.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

function Graph({ data, title, type = 'sentiment', color }) {
  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="graph-container">
        <h3 className="graph-title">{title}</h3>
        <div className="no-data">
          <p>No {type} data available</p>
        </div>
      </div>
    );
  }

  // Convert data object to array format for Recharts
  const chartData = Object.entries(data)
    .map(([year, value]) => ({
      year: parseInt(year),
      value: parseFloat(value) || 0
    }))
    .sort((a, b) => a.year - b.year);

  // Determine colors based on type
  const getColors = () => {
    if (color) return { primary: color, gradient: `${color}40` };
    
    switch (type) {
      case 'sentiment':
        return {
          primary: '#10b981', // Green for sentiment
          gradient: '#10b98140'
        };
      case 'relevancy':
        return {
          primary: '#3b82f6', // Blue for relevancy
          gradient: '#3b82f640'
        };
      default:
        return {
          primary: 'var(--accent-color)',
          gradient: 'var(--glow-color)'
        };
    }
  };

  const colors = getColors();

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const value = payload[0].value;
      const formatValue = () => {
        if (type === 'sentiment') {
          return `${(value * 100).toFixed(1)}%`;
        } else if (type === 'relevancy') {
          return `${value.toFixed(2)}`;
        }
        return value.toString();
      };

      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Year: ${label}`}</p>
          <p className="tooltip-value" style={{ color: colors.primary }}>
            {`${title}: ${formatValue()}`}
          </p>
        </div>
      );
    }
    return null;
  };

  // Format Y-axis labels
  const formatYAxis = (value) => {
    if (type === 'sentiment') {
      return `${(value * 100).toFixed(0)}%`;
    } else if (type === 'relevancy') {
      return value.toFixed(1);
    }
    return value.toString();
  };

  // Get icon based on type
  const getIcon = () => {
    switch (type) {
      case 'sentiment':
        return '😊';
      case 'relevancy':
        return '🎯';
      default:
        return '📊';
    }
  };

  return (
    <div className="graph-container">
      <h3 className="graph-title">
        <span className="graph-icon">{getIcon()}</span>
        {title}
      </h3>
      
      <div className="graph-content">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart
            data={chartData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 20,
            }}
          >
            <defs>
              <linearGradient id={`gradient-${type}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={colors.primary} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={colors.primary} stopOpacity={0}/>
              </linearGradient>
            </defs>
            
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke="var(--glass-border)" 
              opacity={0.3}
            />
            
            <XAxis 
              dataKey="year" 
              stroke="var(--text-secondary)"
              fontSize={12}
              tick={{ fill: 'var(--text-secondary)' }}
            />
            
            <YAxis 
              stroke="var(--text-secondary)"
              fontSize={12}
              tick={{ fill: 'var(--text-secondary)' }}
              tickFormatter={formatYAxis}
            />
            
            <Tooltip content={<CustomTooltip />} />
            
            <Area
              type="monotone"
              dataKey="value"
              stroke={colors.primary}
              strokeWidth={3}
              fill={`url(#gradient-${type})`}
              dot={{
                fill: colors.primary,
                strokeWidth: 2,
                stroke: '#ffffff',
                r: 5
              }}
              activeDot={{
                r: 7,
                stroke: colors.primary,
                strokeWidth: 2,
                fill: '#ffffff'
              }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      
      <div className="graph-summary">
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-label">Years:</span>
            <span className="stat-value">{chartData.length}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Range:</span>
            <span className="stat-value">
              {Math.min(...chartData.map(d => d.year))} - {Math.max(...chartData.map(d => d.year))}
            </span>
          </div>
          <div className="stat">
            <span className="stat-label">Trend:</span>
            <span className={`stat-value trend ${
              chartData[chartData.length - 1]?.value > chartData[0]?.value ? 'positive' : 'negative'
            }`}>
              {chartData[chartData.length - 1]?.value > chartData[0]?.value ? '📈 Rising' : '📉 Declining'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Graph;