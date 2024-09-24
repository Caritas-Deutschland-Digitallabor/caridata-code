/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { AxiosHttpRequest } from './core/AxiosHttpRequest';
import { AggregationsService } from './services/AggregationsService';
import { AuthService } from './services/AuthService';
import { CsrfService } from './services/CsrfService';
import { InvitationsService } from './services/InvitationsService';
import { OrganisationsService } from './services/OrganisationsService';
import { StatisticsService } from './services/StatisticsService';
import { UsersService } from './services/UsersService';
import { VariablesService } from './services/VariablesService';
type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;
export class AppClient {
    public readonly aggregations: AggregationsService;
    public readonly auth: AuthService;
    public readonly csrf: CsrfService;
    public readonly invitations: InvitationsService;
    public readonly organisations: OrganisationsService;
    public readonly statistics: StatisticsService;
    public readonly users: UsersService;
    public readonly variables: VariablesService;
    public readonly request: BaseHttpRequest;
    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = AxiosHttpRequest) {
        this.request = new HttpRequest({
            BASE: config?.BASE ?? '',
            VERSION: config?.VERSION ?? '0.1.0',
            WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
            CREDENTIALS: config?.CREDENTIALS ?? 'include',
            TOKEN: config?.TOKEN,
            USERNAME: config?.USERNAME,
            PASSWORD: config?.PASSWORD,
            HEADERS: config?.HEADERS,
            ENCODE_PATH: config?.ENCODE_PATH,
        });
        this.aggregations = new AggregationsService(this.request);
        this.auth = new AuthService(this.request);
        this.csrf = new CsrfService(this.request);
        this.invitations = new InvitationsService(this.request);
        this.organisations = new OrganisationsService(this.request);
        this.statistics = new StatisticsService(this.request);
        this.users = new UsersService(this.request);
        this.variables = new VariablesService(this.request);
    }
}
