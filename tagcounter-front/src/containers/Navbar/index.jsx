import React, { useState } from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import ModalWindow from '../../components/ModalWindow';



const NavbarMenu = props => {
  const [isOpen, setIsOpen] = useState(false);

  const handleOpenModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <Navbar bg='light' expand='lg'>
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav.Link onClick={handleOpenModal}>About</Nav.Link>
        <ModalWindow
          titleText='About'
          bodyText='Author: Denys Rozlomii'
          handleClose={handleOpenModal}
          isOpen={isOpen}
          />
      </Navbar.Collapse>
    </Navbar>
  )
};

export default NavbarMenu;
