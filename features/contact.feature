Feature: Consultation and Lead Generation Form
  As a facility manager or enterprise project lead
  I want to submit an engineering consultation request
  So that I receive technical proposal review within 4 business hours

  Scenario: Consultation form validation on invalid mobile number
    Given I navigate to the Ananya Electrical Solutions homepage
    When I enter client name "Karnataka Manufacturing Corp"
    And I enter invalid phone number "12345"
    And I enter location "Peenya Industrial Area"
    And I confirm KEI statutory compliance
    And I click submit engineering inquiry
    Then a validation alert should be displayed containing "10-digit Indian mobile number"

