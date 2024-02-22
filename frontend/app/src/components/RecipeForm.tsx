import { Col, Form, InputGroup, Row } from 'react-bootstrap';
import { DirectionsFormGroup } from './DirectionsFormGroup';
import { IngredientsFormGroup } from './IngredientsFormGroup';
import { BadgeStackFormGroup } from './BadgeStackFormGroup';
import { Recipe, recipeTypeLabels } from '../data/recipe_detail';


interface Props {
    recipe?: Recipe,
    withUrlField: boolean
} 


export function RecipeForm({recipe, withUrlField = true}: Props) {

    return (
        <Form className="p-3">
            {
                withUrlField &&
                <Form.Group className="mb-3" controlId="addFromURL">
                    <Form.Label>Add Recipe from URL</Form.Label>
                    <Form.Control type="url" placeholder="type a URL" />
                </Form.Group>
            }
            <Form.Group className="mb-3" controlId="title">
                <Form.Label>Title</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Title"
                    defaultValue={recipe ? recipe.title : ''}
                />
            </Form.Group>
            <Row md={2} xs={1}>
                <Col>
                    <Form.Group className="mb-3" controlId="description">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
                            placeholder="Description"
                            defaultValue={recipe ? recipe.description : ''}
                        />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="notes">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
                            placeholder="Notes"
                            defaultValue={recipe ? recipe.notes : ''}
                        />
                    </Form.Group>
                </Col>
            </Row>
            <Row md={2} xs={1}>
                <Col>
                    <Form.Group className="mb-3" controlId="prepTime">
                        <Form.Label>Preparation Time</Form.Label>
                        <InputGroup>
                            <Form.Control
                                type="number"
                                placeholder="Preparation Time"
                                defaultValue={recipe ? recipe.time_minutes : ''}
                            />
                            <InputGroup.Text>minutes</InputGroup.Text>
                        </InputGroup>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="recipeType">
                        <Form.Label>Type</Form.Label>
                        <Form.Select
                            aria-label="Recipe Type"
                            defaultValue={recipe ? recipe.recipe_type : "default"}
                        >
                            <option key="default" disabled>Recipe Type</option>
                            {['mai', 'sid', 'sal', 'des', 'sna'].map((recipe_type) => (
                                <option
                                    key={recipe_type}
                                    value={recipe_type}
                                >
                                    {recipeTypeLabels[recipe_type]}
                                </option>
                            ))}
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
            {recipe? (
                <>
                    <IngredientsFormGroup ingredients={recipe.ingredients}/>
                    <BadgeStackFormGroup
                        items={recipe.tags}
                        label="Tags"
                        placeholder="Type a new tag and press add."
                    />
                    <DirectionsFormGroup initDirections={recipe.directions} />
                </>
            ) : (
                <>
                    <IngredientsFormGroup />
                    <BadgeStackFormGroup
                        label="Tags"
                        placeholder="Type a new tag and press add."
                    />
                    <DirectionsFormGroup />
                </>
            )}
        </Form>
    )
}
