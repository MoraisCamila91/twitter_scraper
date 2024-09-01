# Requirements
nodejs > 18.0
cypress = 13

# To select which users to scrape
Add the user IDs of the desired users to the script `get_bios/cypress/e2e/spec_getting_users_bios.cy.js` in the `ids` variable (the user ID in the example is that of Elon Musk).

# To run the code
`npx cypress open`

Once Cypress is open:
- Choose E2E Testing
- Select the preferred browser (the code was originally run in Chrome) > Start E2E Testing in [Chosen Browser]
- Select `cypress/e2e/spec_getting_users_bios.cy.js`
