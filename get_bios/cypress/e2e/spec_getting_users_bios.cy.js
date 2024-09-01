const ids = [
    // list of userid of your interest. It should be strings.
    '44196397'
  ];
  describe("template spec", () => {
    ids.forEach((id) => {
      it(`PEGANDO ID DO ${id}`, () => {
        cy.readFile("user_bios.json").then((foojson) => {
          if (foojson[id] || foojson[id] === null) {
            cy.log("JA TENHO");
          } else {
            cy.visit(`https://nitter.poast.org/intent/user?user_id=${id}`, {
              failOnStatusCode: false
            });
            cy.get(".profile-card").then((el) => {
              if (el.find(".profile-bio").length > 0) {
                cy.get(".profile-bio", { timeout: 5000 })
                  .invoke("text")
                  .then((bioText) => {
                    cy.log(bioText); // This will log the text to the Cypress test runner
                    cy.readFile("user_bios.json").then((obj) => {
                      obj[id] = bioText;
                      // write the merged array
                      cy.writeFile("user_bios.json", obj);
                    });
                  });
              } else {
                cy.readFile("user_bios.json").then((obj) => {
                  obj[id] = null;
                  // write the merged array
                  cy.writeFile("user_bios.json", obj);
                });
              }
            });
          }
        });
      });
    });
  });