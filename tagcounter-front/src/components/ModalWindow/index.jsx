import React from 'react';
import PropTypes from 'prop-types';
import { Modal } from 'react-bootstrap';


const ModalWindow = props => {
  const { isOpen, bodyText, titleText, handleClose } = props;

  return (
    <React.Fragment>
      <Modal show={isOpen} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{titleText}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{bodyText}</Modal.Body>
      </Modal>
    </React.Fragment>
  );
};


ModalWindow.propTypes = {
  isOpen: PropTypes.bool,
  bodyText: PropTypes.string,
  titleText: PropTypes.string,
  handleClose: PropTypes.func
};

export default ModalWindow;