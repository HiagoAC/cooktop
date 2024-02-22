import { Col, Form, Row } from 'react-bootstrap';
import { BadgeStackFormGroup } from './BadgeStackFormGroup';


export function SearchForm() {
    return (
        <Form className="p-3">
            <Form.Group className="mb-3" controlId="title">
                <Form.Label>Search by Title</Form.Label>
                <Form.Control type="text" placeholder="Title" />
            </Form.Group>
            <Row md={2} xs={1}>
                <Col>
                    <BadgeStackFormGroup
                        label="Ingredients"
                        placeholder="Type a new ingredient and press add."
                    />
                </Col>
                <Col>
                    <BadgeStackFormGroup
                        label="Tags"
                        placeholder="Type a new tag and press add."
                    />
                </Col>
            </Row>
        </Form>
    )
}
