export type DataItem = {
  [key: string]: any;
};

export type FilterCondition = {
  key: string;
  value: any;
  condition: "=" | "!=";
};

export type AggregationResult = {
  aggregation_id: string;
  organisation_id: string;
  period_level: string;
  period: string;
  value: number;
  upload_id: string;
  grouping_category_1_value?: string;
  grouping_category_2_value?: string;
  grouping_variable_1_id?: string;
  grouping_variable_2_id?: string;
};
