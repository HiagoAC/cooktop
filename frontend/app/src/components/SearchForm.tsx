import { Form } from 'react-bootstrap';
import { IngredientTagInputRow } from './IngredientTagInputRow';


export function SearchForm() {
    return (
        <Form className="p-3">
            <Form.Group className="mb-3" controlId="title">
                <Form.Label>Search by Title</Form.Label>
                <Form.Control type="text" placeholder="Title" />
            </Form.Group>
            <IngredientTagInputRow />
        </Form>
    )
}
