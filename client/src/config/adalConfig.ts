import { AuthenticationContext, AdalConfig } from 'react-adal';

const tenantSubdomain = 'cornellprod';
const clientId = '41e533e7-b473-4087-86a1-c00f86b39487';

const local = window.location.hostname
var redirect = '';

if (local === "localhost") {
    redirect = 'http://localhost:5000/oidc/callback';
    //redirect = 'http://localhost:3000/oidc/callback';
} else {
    redirect = 'https://www.mycourseindex.com/oidc/callback';
}

const adalConfig: AdalConfig = {
    tenant: tenantSubdomain + '.onmicrosoft.com',
    clientId: '41e533e7-b473-4087-86a1-c00f86b39487',
    // redirectUri: 'https://www.mycourseindex.com/oidc/callback',
    // redirectUri: 'http://localhost:5000/oidc/callback',
    redirectUri: redirect,
    endpoints: {
        api: 'https://' + tenantSubdomain + '.onmicrosoft.com/' + clientId,
    },
    cacheLocation: 'sessionStorage'
};

export const authContext = new AuthenticationContext(adalConfig);

export const getToken = () => authContext.getCachedToken(adalConfig.clientId);
