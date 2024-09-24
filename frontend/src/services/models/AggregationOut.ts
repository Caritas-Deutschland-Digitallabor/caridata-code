/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AggregationFilters } from './AggregationFilters';
export type AggregationOut = {
    id: string;
    name: string;
    schema_id: string;
    source: string;
    aggregation_variable_id: string;
    aggregation_variable_name: string;
    description_aggregation?: (string | null);
    description_schema?: (string | null);
    grouping_variable_1_id?: (string | null);
    grouping_variable_2_id?: (string | null);
    is_distinct: boolean;
    aggregation_type?: (string | null);
    filter?: (AggregationFilters | null);
};
