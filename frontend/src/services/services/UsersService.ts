/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UpdateUserIn } from '../models/UpdateUserIn';
import type { UserOut } from '../models/UserOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class UsersService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Get Me
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public getMe(): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/me',
        });
    }
    /**
     * Delete Me
     * @returns void
     * @throws ApiError
     */
    public deleteMe(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/users/me',
        });
    }
    /**
     * Update Me
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public updateMe(
        requestBody: UpdateUserIn,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/users/me',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Users
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public listUsers(): CancelablePromise<Array<UserOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/',
        });
    }
    /**
     * Get User By Id
     * @param id ID des Users
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public getUserById(
        id: string,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update User
     * @param id ID des Users
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public updateUser(
        id: string,
        requestBody: UpdateUserIn,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/users/{id}',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete User
     * @param id ID des Users
     * @returns void
     * @throws ApiError
     */
    public deleteUser(
        id: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/users/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
