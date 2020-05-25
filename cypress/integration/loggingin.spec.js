/// <reference types="cypress" />

describe('Logging In - CSRF Tokens', function () {

    const inMainPage = () => {
        cy.location('href').should('be', '/')
        cy.get('[data-cy="action-dropdown"]')
    }

    const visitMainPage = () => {
        cy.visit('/')
        inMainPage()
    }

    it('redirects to /login', () => {
        cy.visit('/login')
        cy.location('href').should('match', /login\/$/)
    })

    it('403 status without a valid CSRF token', function () {
        // first show that by not providing a valid CSRF token
        // that we will get a 403 status code
        cy.loginByCSRF('invalid-token')
            .its('status')
            .should('eq', 403)
    })

    it('strategy #1: parse token from HTML', function () {
        cy.loginAsAdmin()
        visitMainPage()
    })

    it('strategy #4: slow login via UI', () => {
        // Not recommended: log into the application like a user
        // by typing into the form and clicking Submit
        // While this works, it is slow and exercises the login form
        // and NOT the feature you are trying to test.
        const username = Cypress.env('DJANGO_SUPERUSER_USERNAME')
        const password = Cypress.env('DJANGO_SUPERUSER_PASSWORD')

        cy.visit('/login')
        cy.get('input[name=username]').type(username)
        cy.get('input[name=password]').type(password)
        cy.get('#login-form').submit()
        inMainPage()
    })
})