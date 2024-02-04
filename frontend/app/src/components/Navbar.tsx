import { Container, Nav, Navbar as BaseNavbar, NavDropdown} from 'react-bootstrap'
import '../styles/custom.css';


export function Navbar() {
    return (
        <BaseNavbar expand="lg" className="custom-navbar-bg">
            <Container>
                <BaseNavbar.Brand href="/">
                    Cooktop
                </BaseNavbar.Brand>
                <BaseNavbar.Toggle aria-controls="basic-navbar-nav" />
                <BaseNavbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="/">Meal Plan</Nav.Link>
                        <Nav.Link href="/recipes">Recipes</Nav.Link>
                        <Nav.Link href="/shopping-list">Shopping List</Nav.Link>
                        <Nav.Link href="/pantry">Pantry</Nav.Link>
                    </Nav>
                </BaseNavbar.Collapse>
                <NavDropdown title="Dropdown" id="basic-nav-dropdown" className="ms-auto">
                    <NavDropdown.Item href="/me">User</NavDropdown.Item>
                    <NavDropdown.Item href="/about">About Us</NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="/">Switch Language</NavDropdown.Item>
                    <NavDropdown.Item href="/">Login/Logout</NavDropdown.Item>
            </NavDropdown>
            </Container>
        </BaseNavbar>
    )
}