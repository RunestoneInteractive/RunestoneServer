
# Forked from - Wed Jun 21 09:01:59 EDT 2017
# https://github.com/tophatmonocle/ims_lti_py

# Interestingly, the code in Pypi fails:
# https://pypi.python.org/pypi/ims_lti_py/0.5

# And the code in the Harvard fork fails:
# https://github.com/harvard-dce/dce_lti_py

# But the trunk of this works
# https://github.com/tophatmonocle/ims_lti_py

from lxml import etree, objectify

CODE_MAJOR_CODES = [
    'success',
    'processing',
    'failure',
    'unsupported'
]

SEVERITY_CODES = [
    'status',
    'warning',
    'error'
]

accessors = [
    'request_type',
    'score',
    'message_identifier',
    'response_code',
    'post_response',
    'code_major',
    'severity',
    'description',
    'operation',
    'message_ref_identifier'
]


class OutcomeResponse():
    '''
    This class consumes & generates LTI Outcome Responses.

    Response documentation:
        http://www.imsglobal.org/LTI/v1p1/ltiIMGv1p1.html#_Toc319560472

    Error code documentation:
        http://www.imsglobal.org/gws/gwsv1p0/imsgws_baseProfv1p0.html#1639667

    This class can be used by both Tool Providers and Tool Consumers, though
    each will use it differently. TPs will use it to partse the result of an
    OutcomeRequest to the TC. A TC will use it to generate proper response XML
    to send back to a TP.
    '''
    def __init__(self, **kwargs):
        # Initialize all class accessors to None
        for opt in accessors:
            setattr(self, opt, None)

        # Store specified options in our options member
        for (key, val) in kwargs.iteritems():
            setattr(self, key, val)

    @staticmethod
    def from_post_response(post_response, content):
        '''
        Convenience method for creating a new OutcomeResponse from a response
        object.
        '''
        response = OutcomeResponse()
        response.post_response = post_response
        response.response_code = post_response.status
        response.process_xml(content)
        return response

    def is_success(self):
        return self.code_major == 'success'

    def is_processing(self):
        return self.code_major == 'processing'

    def is_failure(self):
        return self.code_major == 'failure'

    def is_unsupported(self):
        return self.code_major == 'unsupported'

    def has_warning(self):
        return self.severity == 'warning'

    def has_error(self):
        return self.severity == 'error'

    def process_xml(self, xml):
        '''
        Parse OutcomeResponse data form XML.
        '''
        try:
            root = objectify.fromstring(xml)
            # Get message idenifier from header info
            self.message_identifier = root.imsx_POXHeader.\
                imsx_POXResponseHeaderInfo.\
                imsx_messageIdentifier

            status_node = root.imsx_POXHeader.\
                imsx_POXResponseHeaderInfo.\
                imsx_statusInfo

            # Get status parameters from header info status
            self.code_major = status_node.imsx_codeMajor
            self.severity = status_node.imsx_severity
            self.description = status_node.imsx_description
            self.message_ref_identifier = str(
                status_node.imsx_messageRefIdentifier)
            self.operation = status_node.imsx_operationRefIdentifier

            try:
                # Try to get the score
                self.score = str(root.imsx_POXBody.readResultResponse.
                                 result.resultScore.textString)
            except AttributeError:
                # Not a readResult, just ignore!
                pass
        except:
            pass

    def generate_response_xml(self):
        '''
        Generate XML based on the current configuration.
        '''
        root = etree.Element(
            'imsx_POXEnvelopeResponse',
            xmlns='http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0')

        header = etree.SubElement(root, 'imsx_POXHeader')
        header_info = etree.SubElement(header, 'imsx_POXResponseHeaderInfo')
        version = etree.SubElement(header_info, 'imsx_version')
        version.text = 'V1.0'
        message_identifier = etree.SubElement(header_info,
                                              'imsx_messageIdentifier')
        message_identifier.text = str(self.message_identifier)
        status_info = etree.SubElement(header_info, 'imsx_statusInfo')
        code_major = etree.SubElement(status_info, 'imsx_codeMajor')
        code_major.text = str(self.code_major)
        severity = etree.SubElement(status_info, 'imsx_severity')
        severity.text = str(self.severity)
        description = etree.SubElement(status_info, 'imsx_description')
        description.text = str(self.description)
        message_ref_identifier = etree.SubElement(
            status_info,
            'imsx_messageRefIdentifier')
        message_ref_identifier.text = str(self.message_ref_identifier)
        operation_ref_identifier = etree.SubElement(
            status_info,
            'imsx_operationRefIdentifier')
        operation_ref_identifier.text = str(self.operation)

        body = etree.SubElement(root, 'imsx_POXBody')
        response = etree.SubElement(body, '%s%s' % (self.operation,
                                                    'Response'))

        if self.score:
            result = etree.SubElement(response, 'result')
            result_score = etree.SubElement(result, 'resultScore')
            language = etree.SubElement(result_score, 'language')
            language.text = 'en'
            text_string = etree.SubElement(result_score, 'textString')
            text_string.text = str(self.score)

        return '<?xml version="1.0" encoding="UTF-8"?>' + etree.tostring(root)