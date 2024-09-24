export interface IncorrectTypes {
  column: string;
  values: string[];
  expectedType: string;
}
export type RequiredTypes = {
  [key: string]: string;
};
export type ErrorMessages = {
  header: string;
  message: string;
};
