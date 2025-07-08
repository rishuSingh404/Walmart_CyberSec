// Behavioral Metrics Collector for Walmart Secure Integration
// Based on the Flask API documentation

export interface BehaviorMetrics {
  typing_speed: number;
  mouse_distance: number;
  click_count: number;
  typing_interval_variance: number;
  session_duration: number;
  scroll_depth: number;
}

export interface RiskAssessmentMetrics extends BehaviorMetrics {
  ip_location_score?: number;
  device_type_score?: number;
  timestamp?: string;
}

interface KeyPress {
  key: string;
  timestamp: number;
}

interface MousePosition {
  x: number;
  y: number;
}

export class BehaviorCollector {
  private startTime: number;
  private keyPresses: KeyPress[];
  private mouseDistance: number;
  private clickCount: number;
  private scrollDepth: number;
  private lastMousePosition: MousePosition;
  private isCollecting: boolean;

  constructor() {
    this.startTime = Date.now();
    this.keyPresses = [];
    this.mouseDistance = 0;
    this.clickCount = 0;
    this.scrollDepth = 0;
    this.lastMousePosition = { x: 0, y: 0 };
    this.isCollecting = false;
    
    this.initializeListeners();
  }

  private initializeListeners(): void {
    if (typeof window === 'undefined') return;

    this.isCollecting = true;

    // Track key presses
    document.addEventListener('keydown', this.handleKeyPress);
    
    // Track mouse movement
    document.addEventListener('mousemove', this.handleMouseMove);
    
    // Track clicks
    document.addEventListener('click', this.handleClick);
    
    // Track scrolling
    window.addEventListener('scroll', this.handleScroll);
  }

  private handleKeyPress = (event: KeyboardEvent): void => {
    if (!this.isCollecting) return;
    
    this.keyPresses.push({
      key: event.key,
      timestamp: Date.now()
    });
  };

  private handleMouseMove = (event: MouseEvent): void => {
    if (!this.isCollecting) return;
    
    const { clientX, clientY } = event;
    if (this.lastMousePosition.x !== 0 && this.lastMousePosition.y !== 0) {
      const dx = clientX - this.lastMousePosition.x;
      const dy = clientY - this.lastMousePosition.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      this.mouseDistance += distance;
    }
    this.lastMousePosition = { x: clientX, y: clientY };
  };

  private handleClick = (): void => {
    if (!this.isCollecting) return;
    this.clickCount++;
  };

  private handleScroll = (): void => {
    if (!this.isCollecting) return;
    
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
    const clientHeight = document.documentElement.clientHeight;
    
    this.scrollDepth = Math.max(
      this.scrollDepth,
      scrollTop / (scrollHeight - clientHeight) || 0
    );
  };

  public getMetrics(): BehaviorMetrics {
    const sessionDuration = Date.now() - this.startTime;
    
    // Calculate typing speed and variance
    let typingSpeed = 0;
    let typingIntervalVariance = 0;
    
    if (this.keyPresses.length > 1) {
      const intervals: number[] = [];
      for (let i = 1; i < this.keyPresses.length; i++) {
        intervals.push(this.keyPresses[i].timestamp - this.keyPresses[i - 1].timestamp);
      }
      
      // Average interval (typing speed)
      typingSpeed = intervals.reduce((sum, val) => sum + val, 0) / intervals.length;
      
      // Calculate variance
      const mean = typingSpeed;
      const squareDiffs = intervals.map(interval => {
        const diff = interval - mean;
        return diff * diff;
      });
      typingIntervalVariance = Math.sqrt(
        squareDiffs.reduce((sum, val) => sum + val, 0) / intervals.length
      ) / (mean || 1); // Avoid division by zero
    }
    
    return {
      typing_speed: Number(typingSpeed.toFixed(2)),
      mouse_distance: Number(this.mouseDistance.toFixed(2)),
      click_count: this.clickCount,
      typing_interval_variance: Number(typingIntervalVariance.toFixed(4)),
      session_duration: sessionDuration,
      scroll_depth: Number(this.scrollDepth.toFixed(4))
    };
  }

  public getRiskAssessmentMetrics(): RiskAssessmentMetrics {
    const baseMetrics = this.getMetrics();
    const now = new Date();
    
    return {
      ...baseMetrics,
      ip_location_score: 0.95, // Default values - could be enhanced with actual geolocation
      device_type_score: 1.0,  // Default values - could be enhanced with device detection
      timestamp: now.toTimeString().split(' ')[0].substring(0, 5) // HH:MM format
    };
  }

  public reset(): void {
    this.startTime = Date.now();
    this.keyPresses = [];
    this.mouseDistance = 0;
    this.clickCount = 0;
    this.scrollDepth = 0;
    this.lastMousePosition = { x: 0, y: 0 };
  }

  public cleanup(): void {
    this.isCollecting = false;
    
    if (typeof document !== 'undefined') {
      document.removeEventListener('keydown', this.handleKeyPress);
      document.removeEventListener('mousemove', this.handleMouseMove);
      document.removeEventListener('click', this.handleClick);
    }
    
    if (typeof window !== 'undefined') {
      window.removeEventListener('scroll', this.handleScroll);
    }
  }
}

// Singleton instance for global use
let globalCollector: BehaviorCollector | null = null;

export const getBehaviorCollector = (): BehaviorCollector => {
  if (!globalCollector) {
    globalCollector = new BehaviorCollector();
  }
  return globalCollector;
};

export const cleanupBehaviorCollector = (): void => {
  if (globalCollector) {
    globalCollector.cleanup();
    globalCollector = null;
  }
};
