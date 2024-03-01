import { Button, Col, Form, Modal, Row } from 'react-bootstrap';
import { UserPreferencesFormFields } from './UserPreferencesFormFields';


interface Props {
    show: boolean;
    handleClose: () => void;
}


export function SignUpModal({show, handleClose}: Props) {
  
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Sign Up'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Row>
                        <Col>
                            <Form.Group className="mb-3" controlId="firstName">
                                <Form.Label>{'First Name'}</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="First Name"
                                />
                            </Form.Group> 
                        </Col>
                        <Col>
                            <Form.Group className="mb-3" controlId="lastName">
                                <Form.Label>{'Last Name'}</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="Last Name"
                                />
                            </Form.Group> 
                        </Col>
                    </Row>
                    <Form.Group className="mb-3" controlId="emailAddress">
                        <Form.Label>{'Email'}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Email"
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="password">
                        <Form.Label>{'Password'}</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                        />
                    </Form.Group>
                    <UserPreferencesFormFields />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button className="custom_button">
                    {'Create Account'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
