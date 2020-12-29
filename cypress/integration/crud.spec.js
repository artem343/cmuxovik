/// <reference types="Cypress" />

describe('CRUD cmuxes as admin', () => {

    let first_cmux_text = Math.random().toString(36).substring(7)
    let second_cmux_text = Math.random().toString(36).substring(7)

    before(() => {
        cy.loginAsAdmin()
    })

    beforeEach(() => {
        Cypress.Cookies.preserveOnce('sessionid', 'remember_token')
        cy.visit('/')
    })

    it('add cmux', () => {
        cy.get('a[href="/cmux/new/"]').click()
        cy.get('textarea').type(first_cmux_text)
        cy.get('button[type="submit"]').click()
        cy.contains(first_cmux_text)
    })

    it('update cmux', () => {
        cy.get('.update-cmux').first().click()
        cy.get('textarea').clear().type(second_cmux_text)
        cy.get('button[type="submit"]').click()
        cy.contains(first_cmux_text).should('not.exist')
        cy.contains(second_cmux_text)
    })

    it('approve cmux', () => {
        cy.get('.approve-cmux').first().then(firstConfirmButton => {
            cy.wrap(firstConfirmButton).click()
            cy.wrap(firstConfirmButton).should('not.exist')
            cy.get('.alert-success')
        })

    })

    it('search cmux', () => {
        cy.get('[data-cy="main-search"]').type(second_cmux_text)
        cy.get('#main-search-submit').click()
        cy.contains(second_cmux_text)
        cy.contains(first_cmux_text).should('not.exist')
    })

    it('delete cmux', () => {
        cy.contains(second_cmux_text)
        cy.get('.delete-cmux').first().click()
        cy.get('.btn-outline-danger').click()
        cy.contains(second_cmux_text).should('not.exist')
    })



})