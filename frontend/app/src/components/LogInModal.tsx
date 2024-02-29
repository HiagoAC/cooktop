import { Button, Form, Modal } from 'react-bootstrap';


interface Props {
    show: boolean;
    handleClose: () => void;
}


export function LogInModal({show, handleClose}: Props) {
  
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Log In'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
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
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button className="custom_button">
                    {'Log In'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
