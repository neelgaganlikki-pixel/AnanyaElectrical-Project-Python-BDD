Feature: Header Navigation and Modal Drawer
  As a prospective client visiting Ananya Electrical Solutions
  I want to use the header navigation and Enquiry Forms Hub
  So that I can easily discover all available services and modular forms

  Scenario: Enquiry Forms Hub drawer opens with 15 modular forms
    Given I navigate to the Ananya Electrical Solutions homepage
    When I click the Enquiry Forms button in the header
    Then the enquiry hub drawer should be visible
    And the drawer should display 15 modular inquiry options

