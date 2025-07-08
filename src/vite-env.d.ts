/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_FLASK_API_URL: string
  readonly VITE_DEV_MODE: string
  readonly VITE_ANALYTICS_ENABLED: string
  readonly VITE_RISK_THRESHOLD: string
  readonly VITE_ANALYTICS_INTERVAL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
