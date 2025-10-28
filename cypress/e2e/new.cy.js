
describe('Agent Registration Complete Flow', () => {
  const COMPANY_DATA = {
    agency_name: 'Travel Test Agency Ltd',
    first_name: 'John',
    last_name: 'Doe',
    phone: '712345678',
    post_code: '00100',
    address: '123 Test Street',
    city: 'Nairobi'
  };

  const ACCOUNT_DATA = {
    username: 'mercy',
    email: `testuser_${Date.now()}@example.com`,
    password: 'Test@Password123'
  };

  const FILES = [
    '/home/student/Downloads/ID_compressed.pdf',
    '/home/student/Downloads/ID_compressed-1.pdf',
    '/home/student/Downloads/ID_compressed-2.pdf',
    '/home/student/Downloads/ID_compressed-3.pdf',
    '/home/student/Downloads/ID_compressed-4.pdf',
    '/home/student/Downloads/ID_compressed-5.pdf'
  ];

  it('Should complete entire registration flow', () => {
    cy.visit('https://flotravel-test.flocash.com/register');
    cy.viewport(1920, 1080);
    cy.wait(2000);


    cy.log(' === STEP 1: Company Information ===');

    cy.get('input[name="agencyName"]').clear().type(COMPANY_DATA.agency_name);
    cy.get('input[name="firstName"]').clear().type(COMPANY_DATA.first_name);
    cy.get('input[name="lastName"]').clear().type(COMPANY_DATA.last_name);

    cy.contains('Select country code').click();
    cy.wait(300);
    cy.contains('Kenya').click();
    cy.wait(300);

    cy.get('input[name="phone"]').clear().type(COMPANY_DATA.phone);
    cy.get('input[name="postCode"]').clear().type(COMPANY_DATA.post_code);
    cy.get('input[name="city"]').clear().type(COMPANY_DATA.city);
    cy.get('input[name="fullAddress"]').clear().type(COMPANY_DATA.address);

    cy.log('Company Information filled');



    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('required documents');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(1).click();
      }
    });
    cy.wait(1000);





    cy.log(' === STEP 2: Required Documents ===');

    cy.get('input[type="file"]', { timeout: 10000 }).should('have.length.at.least', 1);

    FILES.forEach((fileName, index) => {
      cy.get('input[type="file"]')
        .eq(index)
        .selectFile(`${fileName}`, { force: true });
      cy.wait(300);
      cy.log(`✓ Uploaded file ${index + 1}`);
    });

    cy.log(' Documents uploaded');

    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('create account');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(2).click();
      }
    });
    cy.wait(1000);


    cy.log(' === STEP 3: Create Account ===');

    cy.get('input').then($inputs => {
      cy.log(`Found ${$inputs.length} input fields`);
      $inputs.each((index, el) => {
        const $el = Cypress.$(el);
        cy.log(`Input ${index}: type="${$el.attr('type')}", name="${$el.attr('name')}", placeholder="${$el.attr('placeholder')}", id="${$el.attr('id')}"`);
      });
    });

    cy.get('body').then($body => {
      let usernameField = null;

      if ($body.find('input[name="username"]').length > 0) {
        usernameField = cy.get('input[name="username"]');
      }
      else if ($body.find('input#username').length > 0) {
        usernameField = cy.get('input#username');
      }


      if (usernameField) {
        usernameField.clear().type(ACCOUNT_DATA.username);
        cy.log('Username filled');
      } else {
        cy.log('Could not find username field');
      }
    });

    cy.get('body').then($body => {
      cy.get('input[name="email"]').clear().type(ACCOUNT_DATA.email);
    });
    cy.log(' Email filled');

    cy.get('input[type="password"]').each(($el, index) => {
      cy.wrap($el).clear().type(ACCOUNT_DATA.password);
      cy.log(` Password ${index + 1}`);
    });

    cy.log('Account details filled');


    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('review');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(3).click();
      }
    });
    cy.wait(1000);




    cy.log(' === STEP 4: Review & Submit ===');

    cy.log('Reached Review & Submit page');
    cy.contains(/agree|terms|accept/i).click();
    cy.log('Agreed to terms and conditions');
    cy.log('Registration flow completed successfully!');
  });

  // it('Should submit the registration', () => {
  //   cy.visit('https://flotravel-test.flocash.com/register');
  //   
  //   cy.contains('button', 'Submit').click();
  //   cy.contains('Success', { timeout: 10000 }).should('be.visible');
  // });
});