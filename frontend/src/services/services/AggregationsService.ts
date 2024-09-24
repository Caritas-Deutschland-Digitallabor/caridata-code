/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AggregationOut } from '../models/AggregationOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class AggregationsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * List Aggregations
     * @param source Source of the variable
     * @param schemaId Id of the schema
     * @returns AggregationOut Successful Response
     * @throws ApiError
     */
    public listAggregations(
        source?: 'sbkont' | 'sbkern1' | 'stelle' | 'sbveran' | 'sbkern2',
        schemaId?: (string | null),
    ): CancelablePromise<Array<AggregationOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/aggregations/',
            query: {
                'source': source,
                'schema_id': schemaId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
