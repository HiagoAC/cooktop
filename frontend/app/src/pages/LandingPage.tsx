import { Button, Col, Container, Row } from 'react-bootstrap';
import styles from '../styles/LandingPage.module.css';


export function LandingPage() {
    return (
        <div className={`${styles.main_container}`}>
            <Container className={`${styles.top_container}`}>
                <Row>
                    <Col xs={8}>
                        <div className={`${styles.main_title}`}>CookTOP</div>
                        <div className="px-3">
                            <h2>Make cooking cheaper and faster.</h2>
                        </div>
                    </Col>
                    <Col
                        xs={4}
                        className="d-flex justify-content-end flex-wrap align-items-center"
                    >
                        <Button className="mx-3 mt-3 mb-auto">Sign In</Button>
                        <Button className="mx-3 mt-3 mb-auto">Sign Up</Button>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}
