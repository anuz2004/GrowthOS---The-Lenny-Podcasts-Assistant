export interface GrowthOSError {
  title: string;

  message: string;

  suggestions: string[];

  technical?: string;

  status_code?: number;
}