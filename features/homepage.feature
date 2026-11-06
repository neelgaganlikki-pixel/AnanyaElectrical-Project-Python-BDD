Feature: Homepage Verification
  As an engineering client or visitor
  I want to access Ananya Electrical Solutions homepage
  So that I can review electrical and solar capabilities

  Scenario: Homepage loading and title verification
    Given I navigate to the Ananya Electrical Solutions homepage
    Then the page title should contain "Ananya Electrical Solutions"
    And the brand logo should be visible in the header

