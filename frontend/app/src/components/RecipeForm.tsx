import { Button, Col, Form, InputGroup, Row } from 'react-bootstrap';
import { DirectionsFormGroup } from './DirectionsFormGroup';
import { IngredientsFormGroup } from './IngredientsFormGroup';
import { BadgeStackFormGroup } from './BadgeStackFormGroup';
import { RecipeIn } from '../api/apiSchemas/recipesSchemas';
import { recipeTypes } from '../types/constants'; 
import { Ingredient } from '../types/interfaces';


type RecipeFieldValueMap = {
    [K in keyof RecipeIn]: RecipeIn[K];
};


interface Props {
    recipe: RecipeIn;
    setRecipe: (recipe: RecipeIn) => void;
    withUrlField?: boolean
};


export function RecipeForm({recipe, setRecipe, withUrlField = true}: Props) {

    const handleRecipeChange = <K extends keyof RecipeIn>(
            field: K,
            value: RecipeFieldValueMap[K]
        ) => {
        setRecipe({ ...recipe, [field]: value });
    };

    return (
        <Form className="p-3">
            {
                withUrlField &&
                <Form.Group className="mb-3" controlId="addFromURL">
                    <Form.Label>Add Recipe from URL</Form.Label>
                    <InputGroup className="mb-3">
                        <Form.Control type="url" placeholder="type a URL" />
                        <Button className="custom_button">
                            {'Get Recipe'}
                        </Button>
                    </InputGroup>
                </Form.Group>
            }
            <Row md={3} xs={1}>
                <Col md={7}>
                    <Form.Group className="mb-3" controlId="title">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Title"
                            value={recipe.title}
                            onChange={
                                (e) => (
                                    handleRecipeChange('title', e.target.value)
                                )}
                        />
                    </Form.Group>
                </Col>
                <Col md={3}>
                    <Form.Group className="mb-3" controlId="prepTime">
                        <Form.Label>Preparation Time</Form.Label>
                        <InputGroup>
                            <Form.Control
                                type="number"
                                value={recipe.time_minutes? recipe.time_minutes : 30}
                                onChange={
                                    (e) => (
                                        handleRecipeChange('time_minutes', Number(e.target.value))
                                    )}
                            />
                            <InputGroup.Text>minutes</InputGroup.Text>
                        </InputGroup>
                    </Form.Group>
                </Col>
                <Col md={2}>
                    <Form.Group className="mb-3" controlId="recipeType">
                        <Form.Label>Type</Form.Label>
                        <Form.Select
                            aria-label="Recipe Type"
                            value={recipe.recipe_type}
                            onChange={(e) => handleRecipeChange(
                                'recipe_type', e.target.value)}
                        >
                            {Object.keys(recipeTypes).map((recipe_type) => (
                                <option
                                    key={recipe_type}
                                    value={recipe_type}
                                >
                                    {recipeTypes[recipe_type]}
                                </option>
                            ))}
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
            <Row md={2} xs={1}>
                <Col md={7}>
                    <Form.Group className="mb-3" controlId="description">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
                            placeholder="Description"
                            value={recipe.description? recipe.description : ''}
                            onChange={
                                (e) => (
                                    handleRecipeChange('description', e.target.value)
                                )}
                        />
                    </Form.Group>
                </Col>
                <Col md={5}>
                    <BadgeStackFormGroup
                        items={recipe.tags}
                        setItems={(tags: string[]) => handleRecipeChange('tags', tags)}
                        label="Tags"
                        placeholder="Type a new tag and press add."
                    />
                </Col>
            </Row>
            <Row md={2} xs={1}>
                <Col md={7}>
                    <IngredientsFormGroup
                        ingredients={recipe.ingredients}
                        setIngredients={
                            (ingredients: Ingredient[]) => handleRecipeChange(
                                'ingredients', ingredients)
                        }
                    />
                </Col>
                <Col md={5}>
                    <Form.Group className="mb-3" controlId="uploadImage">
                        <Form.Label>Upload image</Form.Label>
                        <Form.Control type="file" />
                    </Form.Group>
                </Col>
            </Row>
            <Row md={2} xs={1}>
                <Col md={7}>
                    <DirectionsFormGroup
                        directions={recipe.directions}
                        setDirections={
                            (directions: string[]) => handleRecipeChange(
                                'directions', directions)
                        }
                    />
                </Col>
                <Col md={5}>
                    <Form.Group className="mb-3" controlId="notes">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
                            placeholder="Notes"
                            value={recipe.notes ? recipe.notes : ''}
                            onChange={
                                (e) => (
                                    handleRecipeChange('notes', e.target.value)
                                )}
                        />
                    </Form.Group>
                </Col>
            </Row>
        </Form>
    )
}
