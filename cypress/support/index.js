// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

Cypress.Commands.add('loginAsAdmin', () => {
    const username = Cypress.env('DJANGO_SUPERUSER_USERNAME')
    const password = Cypress.env('DJANGO_SUPERUSER_PASSWORD')
    cy.request('/login/')
        .its('body')
        .then((body) => {
            // we can use Cypress.$ to parse the string body
            // thus enabling us to query into it easily
            const $html = Cypress.$(body)
            const csrf = $html.find('input[name=csrfmiddlewaretoken]').val()

            cy.loginByCSRF(username, password, csrf)
                .then((resp) => {
                    expect(resp.status).to.eq(200)
                })
        })
})