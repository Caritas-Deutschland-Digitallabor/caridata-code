/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_reset_forgot_password } from '../models/Body_reset_forgot_password';
import type { Body_reset_reset_password } from '../models/Body_reset_reset_password';
import type { Body_verify_request_token } from '../models/Body_verify_request_token';
import type { Body_verify_verify } from '../models/Body_verify_verify';
import type { CreateUserIn } from '../models/CreateUserIn';
import type { login } from '../models/login';
import type { RegisterUserIn } from '../models/RegisterUserIn';
import type { UserOut } from '../models/UserOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class AuthService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Auth:Db.Login
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public authDbLogin(
        formData: login,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Auth:Db.Logout
     * @returns any Successful Response
     * @throws ApiError
     */
    public authDbLogout(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/logout',
            errors: {
                401: `Missing token or inactive user.`,
            },
        });
    }
    /**
     * Create User
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public createUser(
        requestBody: CreateUserIn,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register User
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public registerUser(
        requestBody: RegisterUserIn,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify:Request-Token
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public verifyRequestToken(
        requestBody: Body_verify_request_token,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/request-verify-token',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify:Verify
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public verifyVerify(
        requestBody: Body_verify_verify,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/verify',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset:Forgot Password
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public resetForgotPassword(
        requestBody: Body_reset_forgot_password,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/forgot-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset:Reset Password
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public resetResetPassword(
        requestBody: Body_reset_reset_password,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/reset-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
}
