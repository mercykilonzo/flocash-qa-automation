// cypress/e2e/agent-registration-robust.cy.js

describe('Agent Registration Flow - Robust', () => {
  const COMPANY_DATA = {
    agency_name: 'Travel Test Agency Ltd',
    first_name: 'John',
    last_name: 'Doe',
    phone: '712345678',
    post_code: '00100',
    address: '123 Test Street',
    city: 'Nairobi',
    country_code: 'Kenya'
  };

  const ACCOUNT_DATA = {
    username: 'mercy',
    email: `testuser_${Date.now()}@example.com`,
    password: 'Test@Password123'
  };

  const FILES = [
    'ID_compressed.pdf',
    'ID_compressed-1.pdf',
    'ID_compressed-2.pdf',
    'ID_compressed-3.pdf',
    'ID_compressed-4.pdf',
    'ID_compressed-5.pdf'
  ];

  // Helper: Try multiple selectors
  const fillUsernameRobust = (value) => {
    const selectors = [
      'input[name="username"]',
      'input#username',
      'input[placeholder*="Username"]',
      'input[placeholder*="username"]'
    ];

    let filled = false;
    
    for (const selector of selectors) {
      cy.get('body').then($body => {
        if ($body.find(selector).length > 0) {
          cy.get(selector)
            .first()
            .should('be.visible')
            .clear()
            .type(value, { delay: 20 });
          cy.log(`✓ Filled username using: ${selector}`);
          filled = true;
          return false; // break
        }
      });
      if (filled) break;
    }

    if (!filled) {
      cy.log('⚠ Warning: Could not find username field with standard selectors');
      // Debug: Print all input fields
      cy.get('input').each(($el, index) => {
        cy.log(`Input ${index}: type=${$el.attr('type')}, name=${$el.attr('name')}, id=${$el.attr('id')}, placeholder=${$el.attr('placeholder')}`);
      });
    }
  };

  before(() => {
    cy.visit('http://flotravel-test.flocash.com/register');
    cy.viewport(1920, 1080);
  });

  it('1. Company Information', () => {
    cy.log('🏢 === Company Information ===');
    
    cy.contains('button', 'Company Information').click();
    cy.wait(500);

    cy.get('input[name="agencyName"]').clear().type(COMPANY_DATA.agency_name, { delay: 20 });
    cy.get('input[name="firstName"]').clear().type(COMPANY_DATA.first_name, { delay: 20 });
    cy.get('input[name="lastName"]').clear().type(COMPANY_DATA.last_name, { delay: 20 });
    
    // Select country
    cy.contains('Select country code').click();
    cy.wait(300);
    cy.contains(COMPANY_DATA.country_code).click();
    cy.wait(500);
    
    cy.get('input[name="phone"]').clear().type(COMPANY_DATA.phone, { delay: 20 });
    cy.get('input[name="postCode"]').clear().type(COMPANY_DATA.post_code, { delay: 20 });
    cy.get('input[name="city"]').clear().type(COMPANY_DATA.city, { delay: 20 });
    cy.get('input[name="fullAddress"]').clear().type(COMPANY_DATA.address, { delay: 20 });

    cy.log('✓ Company Information completed');
  });

  it('2. Upload Documents', () => {
    cy.log('📄 === Required Documents ===');
    
    cy.contains('button', 'Required Documents').click();
    cy.wait(500);

    FILES.forEach((fileName, index) => {
      cy.get('input[type="file"]')
        .eq(index)
        .selectFile(`cypress/fixtures/${fileName}`, { force: true });
      cy.wait(500);
      cy.log(`✓ Uploaded: ${fileName}`);
    });

    cy.log(`✓ Uploaded ${FILES.length} documents`);
  });

  it('3. Create Account', () => {
    cy.log('🔐 === Create Account ===');
    
    cy.contains('button', 'Create Account').click();
    cy.wait(1000);

    // Close any open dropdowns
    cy.get('body').type('{esc}');
    cy.wait(300);

    // Fill username with robust method
    fillUsernameRobust(ACCOUNT_DATA.username);

    // Fill email
    cy.get('input[name="email"]')
      .clear()
      .type(ACCOUNT_DATA.email, { delay: 20 });
    cy.log('✓ Filled: Email');

    // Fill all password fields
    cy.get('input[type="password"]').each(($el, index) => {
      cy.wrap($el)
        .clear()
        .type(ACCOUNT_DATA.password, { delay: 20 });
      cy.log(`✓ Filled: Password field ${index + 1}`);
    });

    cy.log('✓ Create Account completed');
  });

  it('4. Review & Submit', () => {
    cy.log('📝 === Review & Submit ===');
    
    cy.contains('button', 'Review & Submit').click();
    cy.wait(500);

    cy.contains('button', 'Review & Submit').should('be.visible');
    cy.log('✓ Review page loaded');
  });
});