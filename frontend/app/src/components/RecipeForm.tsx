import { Col, Form, InputGroup, Row } from 'react-bootstrap';
import { IngredientTagInputRow } from './IngredientTagInputRow';
import '../styles/RecipeForm.css';


export function RecipeForm() {

    return (
        <Form className="p-3">
            <Form.Group className="mb-3" controlId="addFromURL">
                <Form.Label>Add Recipe from URL</Form.Label>
                <Form.Control type="url" placeholder="type a URL" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="title">
                <Form.Label>Title</Form.Label>
                <Form.Control type="text" placeholder="Title" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="description">
                <Form.Label>Description</Form.Label>
                <Form.Control as="textarea" rows={2} placeholder="Description" />
            </Form.Group>
            <Row md={2} xs={1}>
                <Col>
                    <Form.Group className="mb-3" controlId="prepTime">
                        <Form.Label>Preparation Time</Form.Label>
                        <InputGroup>
                            <Form.Control type="number" placeholder="Preparation Time" />
                            <InputGroup.Text>minutes</InputGroup.Text>
                        </InputGroup>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="recipeType">
                        <Form.Label>Type</Form.Label>
                        <Form.Select aria-label="Default select example">
                            <option>Recipe Type</option>
                            <option value="mai">main dish</option>
                            <option value="sid">side dish</option>
                            <option value="sal">salad</option>
                            <option value="des">dessert</option>
                            <option value="sna">snack</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
        <IngredientTagInputRow />
        </Form>
    )
}
