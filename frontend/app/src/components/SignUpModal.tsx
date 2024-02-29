import { Button, Col, Form, Modal, Row } from 'react-bootstrap';


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
                                <Form.Label>{'FirstName'}</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="First Name"
                                />
                            </Form.Group> 
                        </Col>
                        <Col>
                            <Form.Group className="mb-3" controlId="lastName">
                                <Form.Label>{'LastName'}</Form.Label>
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
                    <Row>
                        <Col>
                            <Form.Group>
                                <Form.Label>
                                    {'How many times a week do you usually to cook?'}
                                </Form.Label>
                                <Form.Control
                                    type="number"
                                    min={1}
                                    max={7}
                                    defaultValue={4}
                                />
                            </Form.Group>
                        </Col>
                        <Col>
                            <Form.Group>
                                <Form.Label>
                                    {'How many servings do you usually cook each time?'}
                                </Form.Label>
                                <Form.Control
                                    type="number"
                                    min={1}
                                    defaultValue={2}
                                />
                            </Form.Group>
                        </Col>
                    </Row>

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
