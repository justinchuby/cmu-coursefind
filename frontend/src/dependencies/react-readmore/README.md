**Expand / collapse, component automatically calculates desired height**

***Props***

All props are optional

****Default Props****

```
collapseText:'Read Less',
expandText:'Read More',
minHeight:'50px',
animation:'1s ease',
className:'react-openclose'
```

|Prop           |What                            |Default          |
|---------------|--------------------------------|-----------------|
|`collapseText` |Text shown in expanded state    |Read Less        |
|`expandText`   |Text shown in collapsed state   |Read More        |
|`minHeight`    |Height in collapsed state       |50px             |
|`animation`    |Css syntax animation prop       |`1s ease`        |
|`className`    |Component ClassName¹            |`react-openclose`|

****CSS (¹)****

Im not going to assume how your CSS loaders are setup;
So style implimentation is up to you, but see below for class names.

```
react-openclose__wrapper : react always needs a container
react-openclose : content conainer
react-openclose--open : open state on container
react-openclose--closed  : open state on container
react-openclose__button : the button
```

***Minimal Example***

```
import ReadMore = from 'react-readmore';

// ...etc

  render() {
    return (
      <ReadMore minHeight="52px" animation="1.2s ease">
        <p>Some <strong>Content</strong>. Obviously, make this more than 52px high worth of content</p>
      </ReadMore>
    );
  }

// ...etc

```
