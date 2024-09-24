export interface Categories {
  value: number;
  text: string;
}

export interface Schema {
  position: number;
  variable_name: string;
  variable_text: string;
  value_type?: string | undefined;
  value_from: number | null;
  value_to: number | null;
  mandatory: boolean;
  categories: Categories[];
  missing: string | null;
}

export type FileSBType =
  | "STELLE"
  | "SBKERN1"
  | "SBKERN2"
  | "SBKONT"
  | "SBVERAN";
