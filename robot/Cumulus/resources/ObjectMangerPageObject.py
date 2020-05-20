import time
from cumulusci.robotframework.utils import capture_screenshot_on_error
from cumulusci.robotframework.pageobjects import BasePage
from cumulusci.robotframework.pageobjects import pageobject
from selenium.webdriver.common.keys import Keys
from BaseObjects import BaseNPSPPage
from NPSP import npsp_lex_locators
from logging import exception


@pageobject("Custom", "ObjectManager")
class ObjectManagerPage(BaseNPSPPage, BasePage):
	
	@capture_screenshot_on_error
	def load_apex_jobs(self):
		"""To go to object manager page for a specific object"""
		url_template = "{root}/lightning/setup/AsyncApexJobs/home"
		url = url_template.format(root=self.cumulusci.org.lightning_base_url)
		self.selenium.go_to(url)
		self.salesforce.wait_until_loading_is_complete()
		self.npsp.wait_for_locator('frame_new', 'vfFrameId', 'vfFrameId')
		self.npsp.choose_frame('vfFrameId')
	
	@capture_screenshot_on_error
	def validate_apex_job_status(self, jobname, status):
		self.npsp.wait_for_apexjob_to_process(jobname, status)
	
	@capture_screenshot_on_error
	def open_fields_and_relationships(self, object_name):
		"""To go to object manager page for a specific object"""
		url_template = "{root}/lightning/setup/ObjectManager/{object}/FieldsAndRelationships/view"
		url = url_template.format(root=self.cumulusci.org.lightning_base_url, object=object_name)
		self.selenium.go_to(url)
		search_button = npsp_lex_locators['object_manager']['global_search']
		self.salesforce.wait_until_loading_is_complete()
		self.selenium.wait_until_page_contains_element(search_button)
	
	@capture_screenshot_on_error
	def create_custom_field(self, type, field_name, related_to):
		search_button = npsp_lex_locators['object_manager']['global_search']
		self.selenium.wait_until_page_contains_element(search_button,60)
		self.selenium.get_webelement(search_button).send_keys(field_name)
		self.selenium.get_webelement(search_button).send_keys(Keys.ENTER)
		time.sleep(1)
		self.salesforce.wait_until_loading_is_complete()
		search_results = npsp_lex_locators['object_manager']['search_result'].format(field_name)
		count = len(self.selenium.get_webelements(search_results))
		if count == 1:
			return
		else:
			locator = npsp_lex_locators['button-with-text'].format("New")
			self.selenium.wait_until_page_contains_element(locator,60)
			self.selenium.get_webelement(locator).click()
			self.salesforce.wait_until_loading_is_complete()
			self.npsp.wait_for_locator('frame_new', 'vfFrameId', 'vfFrameId')
			self.npsp.choose_frame('vfFrameId')
			if type == 'Lookup':
				lookup_locator = npsp_lex_locators['object_manager']['Lookup_option']
				next_button = npsp_lex_locators['object_manager']['button'].format("Next")
				save_button = npsp_lex_locators['object_manager']['button'].format("Save")
				option = npsp_lex_locators['object_manager']['select_related_option'].format(related_to)
				field_label = npsp_lex_locators['object_manager']['input_field_label']
				self.selenium.wait_until_page_contains_element(lookup_locator,60)
				self.selenium.click_element(lookup_locator)
				time.sleep(1)
				self.selenium.click_element(next_button)
				related = npsp_lex_locators['object_manager']['select_related']
				self.selenium.wait_until_page_contains_element(related,60)
				self.selenium.scroll_element_into_view(related)
				self.selenium.get_webelement(related).click()
				self.selenium.click_element(option)
				time.sleep(2)
				self.selenium.click_element(next_button)
				field_label_input = self.selenium.find_element(field_label)
				self.salesforce.populate_field('Field Label', field_name)
				self.salesforce.populate_field('Description', "This is a custion field generated during automation")
				self.selenium.click_element(next_button)
				self.selenium.click_element(next_button)
				self.selenium.click_element(next_button)
				self.selenium.click_element(save_button)
				self.selenium.wait_until_location_contains("FieldsAndRelationships/view", timeout=90,
												   message="Detail page did not load in 1 min")
			
