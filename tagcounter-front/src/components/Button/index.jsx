import React from 'react';
import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";


const SubmitButton = props => {
  const {text} = props;
  
  return (
      <Button variant="primary" {...props}>
        {text}
      </Button>
  )
};

SubmitButton.propTypes = {
  text: PropTypes.string,
};

SubmitButton.defaultProps = {
  text: ''
};

export default SubmitButton;
