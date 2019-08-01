import React from 'react';
import PropTypes from 'prop-types';
import { Form } from 'react-bootstrap';
import SubmitButton from '../Button';


const UrlForm = props => {
  const { onCheck, onClick, isValid, isInvalid } = props;
  return (
      <Form>
        <Form.Group controlId="formBasicUrl" noValidate validated={isValid}>
          <Form.Label>URL address</Form.Label>
          <Form.Control type="url" placeholder="Enter URL" onChange={onCheck} required isInvalid={isInvalid}/>
          <Form.Control.Feedback type="invalid">
            Please enter a correct url.
          </Form.Control.Feedback>
          <Form.Text className="text-muted">
            URL should be starts with http:// or https://
          </Form.Text>
        </Form.Group>
        <SubmitButton variant="primary" type="submit" text="Submit" onClick={onClick}/>
      </Form>
  )
};

UrlForm.propTypes = {
  onCheck: PropTypes.func,
  onClick: PropTypes.func,
  isValid: PropTypes.bool,
  isInvalid: PropTypes.bool
};

export default UrlForm;
