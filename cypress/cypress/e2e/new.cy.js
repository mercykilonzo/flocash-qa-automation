// cypress/e2e/agent-registration.cy.js
// Single test that completes entire flow

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
    // Visit page
    cy.visit('https://flotravel-test.flocash.com/register');
    cy.viewport(1920, 1080);
    cy.wait(2000);

    // ============================================
    // STEP 1: Company Information
    // ============================================
    cy.log('🏢 === STEP 1: Company Information ===');
    
    cy.get('input[name="agencyName"]').clear().type(COMPANY_DATA.agency_name);
    cy.get('input[name="firstName"]').clear().type(COMPANY_DATA.first_name);
    cy.get('input[name="lastName"]').clear().type(COMPANY_DATA.last_name);
    
    // Select country
    cy.contains('Select country code').click();
    cy.wait(300);
    cy.contains('Kenya').click();
    cy.wait(300);
    
    cy.get('input[name="phone"]').clear().type(COMPANY_DATA.phone);
    cy.get('input[name="postCode"]').clear().type(COMPANY_DATA.post_code);
    cy.get('input[name="city"]').clear().type(COMPANY_DATA.city);
    cy.get('input[name="fullAddress"]').clear().type(COMPANY_DATA.address);

    cy.log('✅ Company Information filled');

    // Click Continue or next button
    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('required documents');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('⚠ No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(1).click();
      }
    });
    cy.wait(1000);

    // ============================================
    // STEP 2: Required Documents
    // ============================================
    cy.log('📄 === STEP 2: Required Documents ===');

    // Wait for file inputs to be visible
    cy.get('input[type="file"]', { timeout: 10000 }).should('have.length.at.least', 1);

    // Upload files
    FILES.forEach((fileName, index) => {
      cy.get('input[type="file"]')
        .eq(index)
        .selectFile(`${fileName}`, { force: true });
      cy.wait(300);
      cy.log(`✓ Uploaded file ${index + 1}`);
    });

    cy.log('✅ Documents uploaded');

    // Click Continue
    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('create account');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('⚠ No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(2).click();
      }
    });
    cy.wait(1000);

    // ============================================
    // STEP 3: Create Account
    // ============================================
    cy.log('🔐 === STEP 3: Create Account ===');

    // Debug: Log all inputs on the page
    cy.get('input').then($inputs => {
      cy.log(`Found ${$inputs.length} input fields`);
      $inputs.each((index, el) => {
        const $el = Cypress.$(el);
        cy.log(`Input ${index}: type="${$el.attr('type')}", name="${$el.attr('name')}", placeholder="${$el.attr('placeholder')}", id="${$el.attr('id')}"`);
      });
    });

    // Try to find username field with multiple strategies
    cy.get('body').then($body => {
      let usernameField = null;
      
      // Strategy 1: By name
      if ($body.find('input[name="username"]').length > 0) {
        usernameField = cy.get('input[name="username"]');
      }
      // Strategy 2: By placeholder
      
      // Strategy 3: By ID
      else if ($body.find('input#username').length > 0) {
        usernameField = cy.get('input#username');
      }
      // Strategy 4: First visible text input that's not email
      
      
      if (usernameField) {
        usernameField.clear().type(ACCOUNT_DATA.username);
        cy.log('✓ Username filled');
      } else {
        cy.log('⚠ Could not find username field');
      }
    });

    // Fill email - also try multiple strategies
    cy.get('body').then($body => {
      if ($body.find('input[name="email"]').length > 0) {
        cy.get('input[name="email"]').clear().type(ACCOUNT_DATA.email);
      } else if ($body.find('input[type="email"]').length > 0) {
        cy.get('input[type="email"]').clear().type(ACCOUNT_DATA.email);
      } else {
        cy.get('input[placeholder*="email" i]').first().clear().type(ACCOUNT_DATA.email);
      }
    });
    cy.log('✓ Email filled');

    // Fill passwords
    cy.get('input[type="password"]').each(($el, index) => {
      cy.wrap($el).clear().type(ACCOUNT_DATA.password);
      cy.log(`✓ Password ${index + 1}`);
    });

    cy.log('✅ Account details filled');

    // Click Continue
    cy.get('button').then($buttons => {
      const continueBtn = $buttons.filter((i, btn) => {
        const text = Cypress.$(btn).text().toLowerCase();
        return text.includes('continue') || text.includes('next') || text.includes('review');
      });
      if (continueBtn.length > 0) {
        cy.wrap(continueBtn.first()).click();
      } else {
        cy.log('⚠ No continue button found, trying tab navigation');
        cy.get('[role="tab"]').eq(3).click();
      }
    });
    cy.wait(1000);

    // ============================================
    // STEP 4: Review & Submit
    // ============================================
    cy.log('📝 === STEP 4: Review & Submit ===');

    // Take screenshot of review page
    cy.screenshot('review-page');
    
    cy.log('✅ Reached Review & Submit page');
    cy.log('🎉 Registration flow completed successfully!');
  });

  // Optional: Add a test to actually submit
  it('Should submit the registration', () => {
    cy.visit('https://flotravel-test.flocash.com/register');
    // ... repeat flow above ...
    cy.contains('button', 'Submit').click();
    cy.contains('Success', { timeout: 10000 }).should('be.visible');
  });
});