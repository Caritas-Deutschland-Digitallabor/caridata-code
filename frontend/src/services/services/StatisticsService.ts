/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StatisticsIn } from '../models/StatisticsIn';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class StatisticsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Add Statistics
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public addStatistics(
        requestBody: Array<StatisticsIn>,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/statistics/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
