import {
    Container,
    Nav,
    Navbar as BaseNavbar,
} from 'react-bootstrap';
import '../styles/Navbar.css';
import { Offcanvas } from './Offcanvas';


export function Navbar() {

    return (
        <BaseNavbar expand="lg" sticky="top" className="navbar">
            <Container>
                <BaseNavbar.Brand href="/">
                    Cooktop
                </BaseNavbar.Brand>
                <Nav className="me-auto d-none d-lg-flex">
                    <Nav.Link href="/">Meal Plan</Nav.Link>
                    <Nav.Link href="/recipes">Recipes</Nav.Link>
                    <Nav.Link href="/shopping-list">Shopping List</Nav.Link>
                    <Nav.Link href="/pantry">Pantry</Nav.Link>
                </Nav>
                <Nav>
                    <Offcanvas/>
                </Nav>
            </Container>
        </BaseNavbar>
    )
}
