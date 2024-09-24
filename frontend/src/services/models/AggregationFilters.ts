/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AggregationFilterConditions } from './AggregationFilterConditions';
export type AggregationFilters = {
    operator?: ('AND' | 'OR' | null);
    conditions: Array<AggregationFilterConditions>;
};
