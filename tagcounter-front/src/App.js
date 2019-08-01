import React from 'react';
import './App.css';
import UrlCheck from './containers/UrlCheck';
import { Row, Container, Col } from 'react-bootstrap';
import NavbarMenu from './containers/Navbar';

function App() {
  return (
    <div className='App'>
      <NavbarMenu />
      <Container>
        <Row>
          <Col sm='3'/>
          <Col sm='6'>
            <UrlCheck />
          </Col>
          <Col sm='3'/>
        </Row>
      </Container>
    </div>
  );
}

export default App;
