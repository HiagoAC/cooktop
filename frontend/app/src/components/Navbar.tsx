import { useState } from 'react';
import {
    Button,
    Container,
    Nav,
    Navbar as BaseNavbar,
    ListGroup,
    Offcanvas,
} from 'react-bootstrap';
import '../styles/Navbar.css';
import hamburgerIcon from '../assets/hamburger_icon.svg';


export function Navbar() {
    const [show, setShow] = useState(false);
  
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <BaseNavbar expand="lg" className="navbar">
            <Container>
                <BaseNavbar.Brand href="/">
                    Cooktop
                </BaseNavbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="/">Meal Plan</Nav.Link>
                    <Nav.Link href="/recipes">Recipes</Nav.Link>
                    <Nav.Link href="/shopping-list">Shopping List</Nav.Link>
                    <Nav.Link href="/pantry">Pantry</Nav.Link>
                </Nav>
                <Button className="button-hamburger" onClick={handleShow}>
                    <img src={hamburgerIcon} alt="dropdown" className="icon" />
                </Button>
                <Offcanvas show={show} onHide={handleClose} placement="end">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title></Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    <ListGroup variant="flush" className="offcanvas-list">
                        <ListGroup.Item action href="/">Meal Plan</ListGroup.Item>
                        <ListGroup.Item action href="/recipes">Recipes</ListGroup.Item>
                        <ListGroup.Item action href="/shopping-list">Shopping List</ListGroup.Item>
                        <ListGroup.Item action href="/pantry">Pantry</ListGroup.Item>
                        <ListGroup.Item action href="#">About Cooktop</ListGroup.Item>
                        <ListGroup.Item action href="/me">Account & Settings</ListGroup.Item>
                    </ListGroup>
                </Offcanvas.Body>
                </Offcanvas>
            </Container>
        </BaseNavbar>
    )
}
